---
name: plan-audit
description: Audit whether an implementation matches its original plan by performing a blind reconstruction of the plan from code, then diffing it against the original. Use this skill whenever the user wants to verify code matches a plan, check for scope creep or missing functionality, compare what was built versus what was specified, audit Claude Code output against PLAN.md or SPEC.md, or invokes /plan-audit. Trigger on phrases like "audit my plan", "check if my code matches the plan", "did this implement everything", "any scope creep", "verify implementation", "review against spec", "is my code complete", or any request comparing built code to a planning document. Use this skill even when the user does not explicitly say "audit" but describes wanting to compare implementation against intended design.
---

# Plan Audit

This skill audits whether an implementation matches its plan by inverting the plan-to-code workflow. A blind subagent reconstructs the plan from code alone, and that reconstruction is diffed against the original plan. Differences surface as omissions, additions, vagueness resolutions, and incomplete-implementation signals.

## Why blind reconstruction matters

Forward code review (reading code against a plan) is anchored on the plan. Reviewers checkmark items the plan calls for and tend to miss what is silently absent or silently extra. Blind reconstruction has no anchor: the reconstructor sees only code and must describe what is there. Comparing two descriptions catches what forward review misses.

The skill depends on the reconstructor never seeing the original plan. If blindness fails, the audit collapses into standard code review.

## Bootstrap (check on every invocation, install only if missing)

Before running the workflow, verify the reconstructor subagent is installed.

1. Use the Bash tool to check whether `.claude/agents/plan-audit-reconstructor.md` exists.

2. If it does not exist, inform the user:

   > The plan-audit skill needs a companion subagent that runs in isolation. May I install it now to `.claude/agents/plan-audit-reconstructor.md`? It will be used only by this skill.

3. If the user agrees, copy the bundled definition. The bundled file is in this skill's own `bundled-agents/` directory. For project-level skill installations the source path is `.claude/skills/plan-audit/bundled-agents/plan-audit-reconstructor.md` and the destination is `.claude/agents/plan-audit-reconstructor.md`. For user-level installations the source is `~/.claude/skills/plan-audit/bundled-agents/plan-audit-reconstructor.md` and the destination is `~/.claude/agents/plan-audit-reconstructor.md`. Install at the same scope (project or user) as this skill. Use the Bash `cp` command and confirm the destination file was created.

4. If the user declines, halt and explain the skill cannot proceed without the subagent.

After bootstrap, proceed to Phase 1.

## Workflow

The skill runs end-to-end with one pause for plan confirmation in Phase 2. Do not introduce additional pauses unless something fails.

### Phase 1: Plan discovery

Find the plan in this priority order. Stop at the first hit.

1. **Config-declared path.** If `.claude/plan-audit/config.yaml` exists, read it. If it has a `plan-location` key, use that path. If it has a `plans` list with multiple entries, ask the user which to audit.

2. **Conventional locations.** Look in this order:
   - Most recent file in `.claude/plans/` (sort by mtime)
   - `.claude/plan.md`
   - `PLAN.md`, `SPEC.md`, `DESIGN.md` at the repository root

3. **Conversation history fallback.** If none of the above is found, search the current conversation for a plan-like artifact (a structured description of what should be built, with sections or numbered steps).

If the plan is found only in conversation history, prompt:

> Found plan in conversation history. The audit needs the plan on disk so the reconstructor subagent can be reliably blocked from reading it. Save to `.claude/plans/discovered-{YYYY-MM-DD-HHMM}.md` before proceeding? (y/n)

If the user agrees, save the plan to that path (create `.claude/plans/` if it does not exist). The plan is now a regular plan file at a conventional location, and Phase 2 will create the separate audit snapshot. If the user declines, halt. Explain that the skill cannot work without the plan on disk at a stable location.

### Phase 2: Plan confirmation (the only mandatory pause)

Show the user the discovered plan's path and the first 50 lines or so. Ask:

> Audit against this plan? (y/n) Or specify a different path.

If they confirm, proceed. If they specify a different path, restart Phase 1 with that path as the explicit choice.

Save a timestamped snapshot of the plan to the artifact folder. Folder naming: take the plan's file path, strip any leading dot, then replace all slashes and remaining dots with dashes. For example:

- `PLAN.md` becomes `PLAN-md/`
- `.claude/plans/auth.md` becomes `claude-plans-auth-md/`
- `docs/specs/payment.md` becomes `docs-specs-payment-md/`

The snapshot path: `.claude/plan-audit/{normalized-folder}/original-{YYYY-MM-DD-HHMM}.md`. Create the folder if it does not exist.

### Phase 3: Abstraction inference

Parse the plan section-by-section. For each section, infer an abstraction level using **structural** signals only. Do not use semantic understanding of the content to determine abstraction. Signals:

- Word count per section (short = higher level)
- Density of technical terms, file names, function names, library names
- Presence of acceptance criteria or behavioral specifications
- Number of sub-items and nesting depth

Classify each section as `high-level`, `medium`, or `detailed`.

Build a metadata map in this format:

```
Section: "Authentication"
Abstraction: high-level
---
Section: "Database Schema"
Abstraction: detailed
---
Section: "API Endpoints"
Abstraction: medium
```

This map contains only section names, boundaries, and abstraction tier. It contains zero plan content. The subagent will use it to organize the reconstruction.

**Important:** Do not read any source file contents during this phase. Git metadata (file paths, commit history) is allowed because Phase 4 needs it. Source file contents stay unread until after Phase 5 returns the reconstruction. This prevents code-derived assumptions from biasing the abstraction inference.

### Phase 4: Code scope determination

Determine which files are in scope. Use git, not semantic interpretation. Try in this order:

1. **Plan creation commit.** Run `git log --diff-filter=A --format=%H -- "{plan-path}" | tail -1` to find the commit where the plan file was created. Then `git diff --name-only {commit}..HEAD` to get changed files since plan creation.

2. **Merge-base fallback.** If the plan creation commit is not detectable (plan file was never committed, or has too many recreations), use `git merge-base HEAD main` (or `master`, whichever is the default branch). Then diff from there.

3. **User-supplied base.** If neither works, ask the user for a base reference: "Could not determine code scope automatically. What base commit, branch, or tag should I diff against?"

Save the file list. This becomes one of the inputs to the subagent.

### Phase 5: Subagent invocation

Before invoking the subagent, ensure its permission deny rules cover the active plan path:

1. Read the current `.claude/agents/plan-audit-reconstructor.md`.
2. Check whether the discovered plan path appears in its `permissions.deny` block.
3. If not, prompt the user: "The plan is at a non-standard path ({path}). I need to add a deny rule so the reconstructor cannot read it. May I update the subagent file?"
4. If the user agrees, append deny rules covering the plan path. Add these lines under the `permissions.deny` block in the subagent file, replacing `{path}` with the actual plan path and `{filename}` with the plan file's basename:

   ```yaml
       - Read({path})
       - Bash(cat *{filename}*)
       - Bash(less *{filename}*)
       - Bash(head *{filename}*)
       - Bash(tail *{filename}*)
       - Bash(grep * {path})
   ```

   If they decline, halt.

Also extend the deny rules with any `extra-blocklist` entries from the config file, if present.

Invoke the subagent via the Task tool. The task input includes:

- The file list from Phase 4
- The metadata map from Phase 3
- A direct reference to the subagent's system prompt (which is already in `plan-audit-reconstructor.md`)

Format the task invocation prompt like this:

```
Reconstruct what the code in the following files does, organized into
these sections at the specified abstraction levels.

Files in scope:
{file list, one per line}

Section metadata:
{metadata map}

Follow the constraints in your system prompt. Do not read any planning
files. Output the reconstruction in markdown with the section headers
matching the metadata exactly.
```

The subagent returns the reconstruction. Show it to the user inline. Save it to `.claude/plan-audit/{normalized-folder}/reconstruction-{YYYY-MM-DD-HHMM}.md`.

### Phase 6: Validation and diff

Compare the original plan against the reconstruction using the validation prompt. The full prompt is in `references/validation-prompt.md` of this skill. Read that file and apply it.

The output is a structured audit report with findings categorized by severity (critical, major, minor) and type (omission, addition, vagueness resolution). Sections that have no counterpart in either direction get reported separately.

Save the report to `.claude/plan-audit/{normalized-folder}/diff-{YYYY-MM-DD-HHMM}.md`.

### Phase 7: Output

Show the audit report inline in the conversation. Tell the user where the artifacts are saved (the three files in `.claude/plan-audit/{normalized-folder}/`).

End the skill invocation. Do not offer fixes. Do not interpret findings beyond what is in the report. The user decides what to do.

## Configuration

The skill reads optional configuration from `.claude/plan-audit/config.yaml`. See `references/config-example.yaml` for the schema. The file is optional; without it, the skill uses auto-discovery defaults.

## Subagent Blindness Enforcement

The skill depends on the reconstructor never seeing the original plan. Three layers protect this, in order of strength:

**1. Context isolation (foundation).** The reconstructor is spawned via the Task tool, which gives it a fresh context window. The main agent has the plan in context and cannot serve as the reconstructor. The task input contains only a file list, abstraction metadata, and the reconstruction instruction. No feature name, no description, no PR title, no plan content.

**2. Permission deny rules (primary enforcement).** The reconstructor's YAML frontmatter declares `permissions.deny` rules covering the plan file path, the `.claude/plan-audit/` folder, and common plan naming patterns. Rules block both the Read tool and the corresponding Bash variants (`cat`, `less`, `head`, `tail`, `grep` against blocked paths). Claude Code's permission system enforces these at the application layer.

**3. Validation sanity check (backstop).** Phase 6 of the audit explicitly checks the reconstruction for signs of leakage: near-identical phrasing to the plan, terminology that suggests the subagent saw planning artifacts, or confabulation patterns. The reconstructor itself can also self-flag suspected leaks at the top of its output via "RECONSTRUCTION COMPROMISED." Caught leaks halt the audit and prompt a rerun.

**Optional hardening: worktree isolation.** For users who need stronger guarantees, the reconstructor can be spawned in an isolated Git worktree by adding `isolation: worktree` to its YAML frontmatter in `.claude/agents/plan-audit-reconstructor.md`. The worktree is a temporary clone of the repository with plan files removed, making them physically unreachable rather than just permission-blocked. This closes the Bash-escape-hatch class of failures entirely but adds setup time and disk overhead per audit run. Not default.

**Application-level limitations.** Permission rules are application-level, not OS-level. A determined or confused subagent could theoretically work around them via unanticipated Bash patterns. For the legitimate use case of audit reconstruction, the layered defense above is sufficient. Users with hostile-environment concerns should enable worktree isolation or run Claude Code in a fully sandboxed environment.

## Reference files

- `references/validation-prompt.md`: full text of the Phase 6 validation prompt, applied to compare original vs reconstructed plan
- `references/config-example.yaml`: example configuration file showing all supported keys
- `bundled-agents/plan-audit-reconstructor.md`: subagent definition installed during bootstrap

## Known Risks and Limitations

Acknowledged limitations of the skill. Some have operational handling described below; others are accepted constraints the user should know about.

1. **Conversational-only plans require save-first.** If a plan exists only in chat history, the skill prompts to save before proceeding. Users who refuse cannot use the skill.

2. **Blindness is application-level, not OS-level.** Permission deny rules block documented file-access paths but cannot prevent every theoretical bypass. A determined or confused subagent could theoretically reach plan files via unanticipated Bash patterns. The Phase 6 validation sanity check catches most leaks after the fact. Users who need stronger guarantees should enable opt-in worktree isolation (see Subagent Blindness Enforcement above).

3. **Subagent permission rule fragility.** Documented bugs exist where subagent permission rules are not honored consistently across Claude Code versions (for example, GitHub issue #56686 regarding allow rules outside project root). Deny rules are stricter and less affected, but the underlying system has fragility worth monitoring across versions.

4. **Section names with implementation details leak intent.** Plans with section titles like "Stripe Integration" or "JWT Auth" reveal the vendor or mechanism choice to the reconstructor before reconstruction. Plan authors who need full blindness must use abstract section titles such as "Payment Processing" or "Authentication." The skill does not enforce this.

5. **Plan-as-source-of-truth means stale plans produce noisy diffs.** If a plan was never updated as the code evolved, the audit will report many findings that are actually intentional drift. The user must interpret findings against their knowledge of which decisions were deliberate.

6. **Section matching quality depends on subagent capability.** Semantic section matching requires a capable model. Smaller or less capable models may misalign sections and produce false positives or negatives.

7. **Reconstruction quality determines audit quality.** A poor reconstruction yields a useless audit. The Phase 6 sanity check is the main defense, but subtle reconstruction errors may slip through and produce misleading findings. If the reconstruction looks suspicious, rerun the skill.

8. **Git-derived scope assumes a sane history.** Repositories with no clear plan creation commit, no branch base reference, and no user-provided base ref cannot run the skill without manual intervention. Phase 4 asks the user for a base reference in this case.

9. **Subagent not installed and bootstrap declined.** If the user declines to install the reconstructor subagent during bootstrap, the skill is unusable. Halt cleanly with an explanation; the user can rerun and approve installation later.
