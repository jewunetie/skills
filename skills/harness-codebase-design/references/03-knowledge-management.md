# 03 Knowledge management

This is the first thing to get right and the cheapest thing to fix when wrong. Every coding agent reads project-rooted instruction files at session start: `AGENTS.md` (cross-tool standard), `CLAUDE.md` (Claude Code), `.cursorrules` (Cursor). The contents of these files, plus whatever they point to, shape every decision the agent makes.

## The map-not-manual principle

The single most important lesson from OpenAI's experiment, and from the ETH Zurich study of 138 agentfiles published in February 2026: a giant AGENTS.md is worse than no AGENTS.md.

The OpenAI team tried "one big AGENTS.md" first. It failed in four ways:

1. **Context is scarce.** A bloated instruction file crowds out the actual task, the code, and relevant docs. The agent misses key constraints or optimizes for the wrong ones.
2. **Too much guidance becomes non-guidance.** When everything is "important," nothing is. The agent pattern-matches locally instead of navigating intentionally.
3. **It rots instantly.** A monolithic manual becomes a graveyard of stale rules. The agent cannot tell what is still true; humans stop maintaining it; the file becomes an attractive nuisance.
4. **It is hard to verify.** A single blob does not lend itself to mechanical checks (coverage, freshness, ownership, cross-links), so drift is inevitable.

The ETH Zurich study found this empirically. Across 138 agentfiles tested on real repos:

- LLM-generated agentfiles actively hurt resolution rates while costing 20 percent more tokens.
- Human-written agentfiles helped resolution rates by only about 4 percent.
- Agents spent 14 to 22 percent more reasoning tokens processing context-file instructions, took more steps, and ran more tools, all without improving outcomes.
- Codebase overviews and directory listings did not help. Agents discover repository structure on their own.

The takeaway: AGENTS.md is a table of contents, not an encyclopedia. Roughly 100 lines maximum, often much less. HumanLayer keeps theirs under 60. OpenAI keeps theirs around 100 plus pointers to deeper structured docs.

## What goes in AGENTS.md

AGENTS.md should contain only:

- **Build, test, and lint commands.** Exact commands the agent should run, with no ambiguity. "Run the full build with `./gradlew build`," not "build the project."
- **Pointers to deeper sources of truth.** Links to architecture docs, design specs, plans, references.
- **Hard external constraints.** "Never touch `/legacy`," "always use our logger," "do not remove or edit tests."
- **Tool conventions.** Which CLIs to prefer (`gh`, internal CLIs), which patterns are project-specific.
- **Anything that has caused the agent to fail before.** Each line traces to a specific past failure. Hashimoto's Ghostty AGENTS.md is the canonical public example.

What does NOT go in AGENTS.md:

- Tutorials. The agent is not a junior developer learning the codebase from scratch.
- Codebase structure listings. Agents navigate fine.
- Aspirational guidelines that nobody enforces.
- Long explanations of why things are the way they are. Save those for the docs the AGENTS.md points to.
- Generated content. LLM-generated AGENTS.md files actively hurt performance per the ETH Zurich data.

## Conditional rules and monorepo composition

For larger codebases, almost all rules should be scoped to subdirectories rather than applied unconditionally. OpenAI's repo uses 88 AGENTS.md files across subcomponents. Stripe applies rules conditionally based on file paths. The unconditional, top-level AGENTS.md should contain only universally applicable rules. Per-domain AGENTS.md files in subdirectories handle domain-specific conventions.

## The docs system of record

AGENTS.md points to a structured `docs/` directory. The docs directory is the system of record. Anything the agent might need to know that is not a one-liner lives here.

A starter layout (adapt to the project, do not copy verbatim):

```text
AGENTS.md                          # 100 lines, table of contents
ARCHITECTURE.md                    # top-level map of domains and package layering
docs/
  design-docs/
    index.md                       # catalog with verification status per doc
    core-beliefs.md                # agent-first operating principles
    [topic].md
  exec-plans/
    active/                        # in-flight execution plans
    completed/                     # archive
    tech-debt-tracker.md           # known debt, versioned
  product-specs/
    index.md
    [feature].md
  generated/                       # auto-generated, do not hand-edit
    db-schema.md
  references/                      # vendored LLM-readable refs for external deps
    [framework]-llms.txt
  QUALITY_SCORE.md                 # graded quality per domain or layer
  PRODUCT_SENSE.md                 # product principles the agent applies
```

A few load-bearing details:

- **Design docs are catalogued and indexed**, with verification status. This lets the agent (and a doc-gardening agent) tell what is still true.
- **A "core beliefs" file** captures agent-first operating principles. It is short and stable.
- **A quality document** grades each domain and tracks gaps over time. This gives the agent (and humans) a running view of where work is needed.
- **A `references/` directory** holds vendored, LLM-readable docs for major dependencies. This means the agent does not need to fetch docs at runtime, which is slow and unreliable.
- **Plans are first-class versioned artifacts.** Lightweight ephemeral plans for small changes. Heavier execution plans (with progress logs and decision history) for complex work. Co-locating active, completed, and tech-debt plans lets the agent operate without external context.

## State files: JSON over Markdown

When the agent needs to read and update structured state across sessions (a feature list, a progress tracker, a checklist of acceptance criteria), use JSON, not Markdown.

Anthropic's experiments found that models are less likely to inappropriately rewrite, reformat, or accidentally edit JSON files. Markdown invites prose drift. JSON forces edits to be structural.

Their canonical pattern: a JSON feature list with one entry per testable behavior, every entry initially marked failing.

```json
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
  }
```

Strongly-worded behavioral instruction in AGENTS.md:

> The agent edits this file only by changing the status of a `passes` field. It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality.

Anthropic used over 200 such entries for a claude.ai clone. Each agent session worked on a single failing entry, marked it passing only after end-to-end verification, and committed.

## The startup ritual

For long-running or multi-session work, every coding-agent session should run a fixed set of "get your bearings" steps before doing anything. This saves tokens (the agent does not have to figure out how to test the code) and prevents the "implement on top of broken state" failure mode.

A standard ritual:

1. `pwd` to confirm directory.
2. Read `claude-progress.txt` (or equivalent progress file) to see what was done last.
3. Read the feature list to see what is still failing.
4. `git log --oneline -20` to see recent commits.
5. Run `init.sh` to start the dev server.
6. Run a basic smoke test (open the app, exercise one critical path) to confirm the codebase is not in a broken state.
7. Only then start new work.

The `init.sh` should be written by an initializer agent on the first session and committed. See `references/08-long-running-coordination.md`.

## Pushing context into the repo

The orienting principle, from OpenAI: from the agent's point of view, anything it cannot access in-context while running effectively does not exist.

This means knowledge in Slack threads, Google Docs, and people's heads is invisible to the agent. The agent sees only repository-local versioned artifacts (code, markdown, schemas, executable plans). Useful framing: a Slack discussion that aligned the team on an architectural pattern is illegible to an agent in the same way it would be illegible to a new hire joining three months later.

The lesson is to push context into the repo over time. When the team makes an architecture decision, write it down somewhere the agent can find it. When a senior engineer's opinion shapes a review, encode that opinion in a doc or a lint.

This is not about overwhelming the agent with documentation. It is about organizing and exposing the right information so the agent can reason over it. The new-hire onboarding analogy carries through: you would not give a new hire a 1,000-page manual, but you would give them an architecture overview, a list of tech-debt items, and a short note on team conventions.

## Vendored references for dependencies

For dependencies whose docs the agent needs to consult often (a design system, a build tool, a framework), vendor the LLM-readable version of the docs into `docs/references/`. OpenAI's repo includes files like `design-system-reference-llms.txt`, `nixpacks-llms.txt`, `uv-llms.txt`.

This pattern is faster than the agent fetching docs from the web, more reliable than relying on training data (which is often outdated for niche libraries), and pinnable to a known version.

## Mechanical doc enforcement

Documentation rots without active maintenance. Two mechanisms keep the docs system honest:

- **Linters and CI jobs** that validate cross-links, freshness markers, and structural correctness. Broken doc references fail the build.
- **A scheduled "doc-gardening" agent** (small team and up) that scans for stale or obsolete documentation that no longer reflects code behavior, and opens fix-up PRs.

The doc-gardening agent runs on a regular cadence, not on every commit. It is the documentation equivalent of garbage collection.

## Solo developer minimum

A solo developer does not need most of this. The minimum that earns its place:

- A short AGENTS.md or CLAUDE.md (under 100 lines, often under 60). Build commands, test commands, hard constraints, anything the agent has gotten wrong before.
- A single `docs/` folder for design notes that exceed AGENTS.md's space budget.
- Plans in `docs/exec-plans/` only for work that spans multiple sessions.

Skip JSON feature lists, doc-gardening agents, vendored references, and quality grading until the codebase is large enough that they earn their place.
