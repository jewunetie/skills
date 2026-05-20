# 09 Garbage collection and golden principles

Agents replicate whatever patterns already exist in the codebase, including suboptimal ones. Over time, this produces drift: small inconsistencies compound into systemic divergence. Documentation goes stale. Utilities get reinvented. Naming conventions slip. Architectural rules get bent.

Drift is inevitable in any agent-generated codebase. The question is how to manage it cheaply.

## The high-interest-loan framing

OpenAI's mental model is worth adopting verbatim: technical debt is a high-interest loan. It is almost always better to pay it down continuously in small increments than to let it compound and tackle it in painful bursts.

Daily small payments catch and resolve bad patterns before they spread for days or weeks. Weekly cleanup days do not scale. The OpenAI team initially spent every Friday (about 20 percent of the week) cleaning up "AI slop" manually. It did not work. They replaced the model.

## Manual cleanup does not scale

Recognize the failure mode early. Symptoms that you have hit it:

- The team blocks out a "cleanup day" weekly or monthly.
- Cleanup days run over time. Backlog grows.
- Senior engineers spend disproportionate time on style and consistency review rather than substantive work.
- The same kind of inconsistency keeps appearing in different parts of the codebase.
- "We need to refactor X" comes up in retros repeatedly without progress.

When these show up, manual cleanup is the bottleneck. The fix is to encode the cleanup as a continuous mechanical process.

## Golden principles

The replacement for manual cleanup: encode opinionated, mechanical rules in the repo. These are the "golden principles" the codebase keeps consistent over time. They are different from architectural constraints (which are about correctness) and from taste invariants (which are about what to lint). Golden principles are about what the codebase wants to look like.

Two named examples from OpenAI:

1. **Prefer shared utility packages over hand-rolled helpers.** Keeps invariants centralized. When the agent needs a function it has written before, it goes to the utility package rather than reinventing it. When a new helper is needed, it is added to the utility package, not inline.

2. **Do not probe data shapes "YOLO-style".** Validate at boundaries or rely on typed SDKs so the agent cannot accidentally build on guessed shapes. Encoded as a constraint that triggers when the agent attempts to access fields on an unknown shape.

A starter set worth considering for any project:

- **Centralize cross-cutting concerns.** Auth, logging, telemetry, feature flags go through Providers (or whatever the project calls them), not inline.
- **Reuse before creation.** Search the utility package before writing a new helper.
- **Boundary validation.** Data crossing a layer or external boundary is validated and typed.
- **No silent error swallowing.** Every catch logs or re-throws.
- **Stable test idioms.** New tests follow the structure of existing tests. No reinventing test helpers.
- **Naming consistency.** A `User` model has one canonical name everywhere. No `Customer`, `Account`, `Person` for the same concept.
- **One way to do common things.** HTTP requests through the project HTTP client. Database access through the project ORM/query builder. Time through the project clock abstraction.

The principles are opinionated by design. There are usually multiple acceptable patterns; pick one and enforce.

## Scheduled cleanup agents

The mechanism that makes golden principles cheap: agents that run on a schedule, scan for deviations, and open targeted refactor PRs.

OpenAI's pattern:

- A set of background Codex tasks runs on a regular cadence (daily or hourly).
- Each task scans the repo for a specific class of deviation: stale documentation, golden-principle violations, naming drift, files exceeding size limits, etc.
- Violations trigger a refactor PR. The PR is small (one violation, one fix).
- The PR is reviewable in under a minute and can be auto-merged after passing CI.

Each cleanup agent is targeted. Do not write a generic "find and fix problems" agent. Write specific ones:

- "Find files that have a hand-rolled helper duplicating a utility-package function. Replace the helper with the utility-package call."
- "Find documentation files that reference functions that no longer exist. Remove the dead references."
- "Find tests that have been skipped (`.skip` or `xit`) for more than 30 days. Open an issue if the test is still in the codebase, or remove if obsolete."
- "Find files exceeding the size limit. Propose a decomposition."

Each agent has a narrow scope and a clear stopping condition. Each PR is mergeable on its own.

## Quality grading

The complementary pattern: maintain a `QUALITY_SCORE.md` (or similar) that grades each domain or layer of the codebase. The grades are updated by a scheduled agent.

A grade includes:

- The current score (often a letter grade or a number out of 10).
- Specific gaps: "the auth domain has three TODO comments older than 60 days, two functions exceeding the size limit, and missing structured logging in two places."
- A trend: improving or degrading.

The grade gives humans (and the agent) a running view of where work is needed. It is itself a form of back-pressure: a degrading grade triggers attention.

## What the cleanup agent should NOT do

A few classes of cleanup are bad ideas to automate:

- **Wholesale reformatting**: agents will sometimes reformat huge swaths of code in ways that pass tests but break review hygiene. Restrict the cleanup agent's diff to the specific lines containing violations.
- **Behavior changes**: a cleanup agent that touches production behavior is dangerous. Restrict to mechanical, behavior-preserving changes.
- **Touching tests**: the strongly-worded constraint from earlier applies. Cleanup agents should not edit test logic, only refactor non-test code.
- **Cross-domain refactors**: if a refactor crosses domain boundaries, it deserves human review, not auto-merge.
- **Touching files marked stable**: a `STABLE.md` or per-file marker can opt files out of cleanup.

The cleanup agent is not for everything. It is for one class of mechanical, behavior-preserving changes.

## The continuous cycle

Once golden principles, scheduled cleanup, and quality grading are in place, the cycle becomes:

1. Agent generates code, including small inconsistencies.
2. CI passes the code; humans review and merge it (or auto-merge if simple).
3. The next scheduled cleanup run finds the inconsistencies.
4. A small refactor PR fixes them. Auto-merges after CI.
5. Quality grade is updated. Where it degrades, attention follows.
6. Repeat.

The goal: human taste is captured once, then enforced continuously on every line of code.

## Drift as feedback

When the cleanup agent keeps finding the same kind of violation, that is a signal. The pattern probably needs to be promoted from a golden principle (corrective) to a custom lint or architectural rule (preventive). Move it to `references/04-architectural-enforcement.md` territory.

This is the same diagnostic loop from earlier: if a constraint keeps failing, the constraint has the wrong shape. Make it more legible and more enforceable.

## Solo developer minimum

A solo developer probably does not need scheduled cleanup agents. The minimum that earns its place:

- A `STYLE.md` or short list of three to five golden principles in AGENTS.md.
- Manual review of agent-generated code with a "promote rule when you see drift" discipline. When you find yourself fixing the same kind of thing twice, encode it.

Scale up to scheduled cleanup once the team is large enough that manual drift-correction takes more than an hour a week.

## Retrofitting drift to an existing codebase

If you are inheriting a codebase with substantial drift already in place, do not try to clean it all at once. The pattern from `references/04-architectural-enforcement.md` applies: pick one class of drift, write the cleanup agent for it, run it iteratively over weeks. Drain the violation backlog. Then pick the next class.

The PR-per-violation pattern is especially valuable for legacy debt because each PR is small and reviewable. Reviewers can stomach 30 small auto-mergeable cleanup PRs in a week. They cannot stomach one 30,000-line "fix everything" PR.
