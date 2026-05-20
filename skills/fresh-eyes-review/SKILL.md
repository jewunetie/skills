---
name: fresh-eyes-review
description: Multi-pass self-review of work Claude just produced or modified, looking for bugs, errors, inconsistencies, and confusion. Trigger whenever the user says "fresh eyes review", "read carefully over what you just wrote", "look for any obvious bugs/errors/issues/problems", "review what you just modified", or "critically examine" what was just produced. Also trigger on prompts asking Claude to review work for typos, ambiguous wording, missing context, conflicting information, output-format inconsistencies, or logical/structural bugs. Also use proactively after producing a substantial deliverable (code file, document, slide deck, skill, spec, prompt). The skill runs a structured sequence of focused passes (surface, logic, cross-reference, regression) rather than one generic pass, because LLM self-critique misses different categories of issues on different passes. Do not use for trivial outputs like a one-sentence answer or a single-line edit.
---

# Fresh Eyes Review

Iterative self-review of work Claude just produced or modified. The skill runs a sequence of focused passes, fixing what each pass finds, until a final sweep finds nothing worth fixing.

## Why multiple passes

A single pass with a generic "find errors" prompt has known failure modes:

1. **Self-bias.** The model tends to favor and rationalize its own initial output. One pass is rarely enough to overcome this.
2. **Surface bias.** A single generic pass tends to catch typos and formatting but miss deeper logic and consistency errors.
3. **Regression.** Fixes introduced in one round can themselves contain new bugs. Without a dedicated regression pass, these slip through.
4. **Sycophantic completion.** Claude often declares a review complete after one pass with phrases like "the document looks clean and error-free" without having actually re-read carefully.

Multiple focused passes address each of these. Different passes look for different categories of issues. Each pass treats the output as if seeing it for the first time.

## Step 1: Enumerate scope

Before the first pass, output an explicit scope block listing every file, artifact, or text section in scope. This counters the common failure mode where Claude reviews only the most recent thing and forgets earlier modifications in the same conversation.

Format:

```
Scope:
- /path/to/file1 (created this turn)
- /path/to/file2 (modified earlier this conversation)
- artifact: name-of-artifact (last edited 2 turns ago)
- inline text: response in turn N
```

If the scope is empty (nothing was produced or modified), say so and stop. Do not invent scope.

If the scope is ambiguous, ask the user before starting. Reviewing the wrong thing wastes the effort.

## Step 2: Identify artifact type

Pick one or more types from the table below. Multiple types can apply at once. For each type that applies, read the corresponding reference file before starting the passes.

| Type | Reference file |
|------|----------------|
| Code (any language, including scripts in skills) | references/code-review.md |
| Prose, notes, documents, articles, emails | references/prose-review.md |
| Skill, spec, prompt, instructions, agent config | references/skill-spec-review.md |
| Slides, decks, presentations | references/slides-review.md |

The reference files contain the per-category checklists that drive each pass. Without them, the passes degrade into a generic "look for errors" prompt, which is exactly the failure mode this skill exists to prevent.

## Step 3: Run focused passes

Each pass has a single focus. Run them in order. After each pass, fix the issues found, then start the next pass.

**Read the whole artifact each pass, not just the diff.** A change that is correct in isolation can be inconsistent with unchanged content elsewhere. The point of fresh eyes is to read the artifact as a reader would encounter it for the first time, not to inspect only what was edited.

Each pass must produce a structured report. The report is the proof that the pass actually happened. A pass that ends with "looks clean" without naming the categories checked is not a real pass and must be redone.

### Pass 1: Surface

Use the categories listed under "Pass 1: Surface" in the reference file for the artifact type. Typical examples across artifact types: typos, grammar, formatting violations (em-dashes, emoji, contractions if user prefers none), broken markdown or code syntax, dangling references, inconsistent capitalization or terminology.

Apply user formatting preferences from the conversation (userPreferences, prior instructions). Do not assume defaults; check the actual preferences in this session.

### Pass 2: Logic and internal consistency

Use the categories listed under "Pass 2: Logic and internal consistency" in the reference file for the artifact type. Typical examples: does the output do what it claims, are steps in the correct order, do later sections contradict earlier ones, are off-by-one or edge-case errors present, are introduced names actually used, are used names actually introduced.

This pass is read-only against the artifact, but requires careful reading rather than skimming. If a pass takes only a few seconds, it probably skimmed.

### Pass 3: Cross-reference

Compare the artifact against external authority:

- The user's original request: did the output address every part of it?
- The user's stated preferences in this conversation
- Source files, past chats, or specifications the output should be consistent with
- Documentation or external standards the output references

This pass requires actually opening other files or running searches. Do not produce a Pass 3 report without having checked at least one external reference. If nothing external applies, state that explicitly and explain why.

### Pass 4: Regression

Re-read the whole artifact one more time, paying special attention to the fixes from Passes 1-3 and their neighbors. The point of this pass is not to re-examine every category, but to ask: did the previous passes' fixes create new problems? Categories: new typos introduced by edits, partial replacements that left old wording behind, fixes that conflict with unchanged content elsewhere, references that became stale because a section was renamed or moved, neighboring content broken by a `str_replace`.

Do not skip this pass even if the prior passes found nothing, because the absence of fixes does not mean the absence of new issues from any unrelated work in the same conversation.

## Step 4: Final sweep and termination

After Pass 4, run one consolidated sweep over all four categories. If that sweep finds nothing worth fixing, the review is complete and Claude outputs the closing line specified in Reporting format.

If the final sweep finds new issues, loop back to whichever pass owns the category, fix, then re-run Pass 4 and the final sweep again. Each loop-back plus its sweep counts as one cycle. If a final-sweep finding spans multiple categories (for example, a regression that introduced both a typo and an inconsistency), pick the pass whose category dominates and re-run from there; Pass 4 will catch any spillover.

**Hard cap: 5 total cycles, where the initial Pass 1 through final-sweep run is cycle 1 and each subsequent loop-back is cycle 2, 3, and so on.** Beyond cycle 5, stop and surface remaining issues to the user without attempting further fixes. The loop is not converging and human judgment is needed.

## Reporting format

Each pass reports in this structure:

```
Pass N (focus): X issues found and fixed, Y questions raised.

Categories checked: <comma-separated list, naming each category from the reference file that was actually examined for this artifact>

Fixes:
- [specific issue]: [specific fix]
- [specific issue]: [specific fix]

Questions (if any):
- [issue Claude is unsure about]
```

The categories list should name the actual checklist items the pass walked through, not just the pass title. If a category was not applicable to this artifact, omit it; do not pad the list. The point is to make the report verifiable, so a reader can ask "did you actually check X" and see whether X is on the list.

Two rules for the report:

1. **Be specific.** "Fixed typo" is not enough. "Replaced 'recieve' with 'receive' on line 42" is. Specificity is what makes the report verifiable.
2. **Surface uncertainty as questions.** If a pass finds something that might be wrong but might be intentional, do not silently fix it. Ask. Example: "Section 'Setup' says max 5 iterations, but 'Termination' says max 4. Which is correct?"

When the review is complete, output a single closing line in this format:

```
Fresh eyes review complete. <total fixes across the whole review> total fixes across <number of cycles> cycles.
```

Use cycles, not passes, in the closing line so multi-cycle runs report cleanly.

## Gotchas

These are real failure modes from past use. Watch for them.

1. **Sycophantic clean pass.** When prior passes found nothing, Claude often returns "Reading through one more time with completely fresh eyes, the document looks clean and error-free!" without actually re-reading. Counter: every pass must explicitly enumerate the categories checked. A pass without that enumeration is not a real pass and must be redone.

2. **Scope drift.** Claude reviews only the most recently written file and forgets earlier modifications. Step 1 (explicit scope enumeration) is the fix. If the scope block has only one item but the conversation involved editing multiple files, recheck before proceeding.

3. **Format leak in fixes.** A common case: the original output complies with user preferences (no em-dashes, no contractions) but the fix introduces a violation. Pass 4 catches this if Pass 4 is actually run.

4. **Cross-reference skipped.** Pass 3 requires actually opening other files or searching past chats. A Pass 3 that takes a few seconds and produces no findings probably did not run. Either actually do the cross-reference, or state explicitly that no external reference applies and why.

5. **False completion.** Claude declares the review done after one pass found nothing. Real completion requires Pass 4 plus the final sweep, even if Passes 1-3 were clean. Do not short-circuit.

6. **New bugs from fixes.** A `str_replace` that "looks right" can break neighboring content (broken markdown lists, partially replaced strings, references to renamed sections). After every meaningful edit, re-read the surrounding context, not just the diff.

7. **Looking only at the diff.** Reviewing only what changed misses cases where the change was correct in isolation but inconsistent with unchanged content. Each pass should consider the artifact as a whole, not just the recent edits.

8. **Conflating passes.** Running all four categories in a single pass defeats the purpose of the skill. Each pass has its own focus. Discipline matters here.

## Relationship to other skills

The `ralph-wiggum` skill provides general-purpose iteration with formal state tracking (a JSON state file) and a `<promise>` completion signal. Use ralph-wiggum when the work needs an externally tracked iteration cap that survives even if conversation context is compacted, when the task is open-ended rather than a structured review, or when the completion criterion is something other than "no issues found."

Use this skill (`fresh-eyes-review`) when the review fits in one conversation and the artifact type is one of the supported scopes. The two can be combined: ralph-wiggum for the outer loop, fresh-eyes-review for the inner review structure within each iteration.
