# 08 Long-running and multi-agent coordination

For tasks that span more than one context window, the harness has to bridge sessions. Each new agent session starts with no memory of what came before. Without explicit scaffolding, the agent will either try to one-shot the task (and fail when the context runs out) or look at partial progress and declare victory prematurely.

This reference covers the patterns for keeping an agent on task across hours or days of autonomous work, plus the multi-agent patterns that further extend reach.

## The two failure modes to design around

From Anthropic's experiments with Opus 4.5 trying to build a claude.ai clone:

1. **One-shotting**: the agent tries to do too much in a single session, runs out of context mid-implementation, leaves the codebase half-built. The next session has to figure out what happened, often spending substantial time getting basic features working again.
2. **Premature completion**: a later session sees that some progress has been made, looks around briefly, and declares the project done. This happens reliably without explicit scaffolding to prevent it.

A third failure mode worth knowing about: **context anxiety**. The Cognition team (Devin) documented this in Sonnet 4.5: as the context window fills, the model becomes aware it is approaching the limit and starts wrapping up tasks prematurely, even when there is plenty of room. Opus 4.6 largely removed this behavior, but it is worth checking whether your model exhibits it.

## The initializer / coding agent pattern (small team and up)

Anthropic's solution for the failure modes above is a two-fold harness:

**Initializer agent**: runs only on the very first session. Its job is to set up the durable environment that all later sessions will read from. The initializer creates:

- An `init.sh` script that starts the dev server and runs basic smoke tests.
- A `claude-progress.txt` file (initially empty or with a baseline note).
- An initial git commit establishing a baseline.
- A comprehensive feature list (JSON, see below) expanding the user's prompt into hundreds of testable behaviors, all initially marked failing.

**Coding agent**: runs on every subsequent session. Its job is to make incremental progress on one feature at a time, then leave the environment in a clean state for the next session.

These are not literally separate agents. Anthropic's note: same underlying agent harness, same tools, same system prompt. The difference is the user prompt. The first prompt is "set up the environment." All subsequent prompts are "make incremental progress."

## The session startup ritual

Every coding-agent session runs a fixed set of "get your bearings" steps before doing any work. This saves tokens (the agent does not figure out testing on every session) and prevents implementing on top of broken state.

Standard ritual:

```text
1. pwd                                  (confirm directory)
2. read claude-progress.txt             (what was done last)
3. read feature_list.json               (what is still failing)
4. git log --oneline -20                (recent commits)
5. ./init.sh                            (start dev server)
6. run a basic smoke test               (open app, exercise critical path)
7. only then start new work
```

Encoded as instructions in AGENTS.md or in the coding-agent prompt. Strongly worded: "Run these steps before any work. Do not skip them."

## Feature list as the source of truth

The structured-state pattern that makes long-running coding work:

- A JSON file with one entry per testable behavior.
- Each entry has a description, verification steps, and a `passes` boolean.
- Initial state: every feature `passes: false`.
- The agent picks one failing feature per session.
- The agent edits this file only by changing the `passes` field after verifying end-to-end.

A concrete example from Anthropic's claude.ai clone (over 200 features):

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

Strongly worded constraint in AGENTS.md:

> It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality. The agent edits this file only by toggling the passes field after verifying end-to-end.

JSON is preferred over Markdown because models are less likely to reformat or accidentally rewrite JSON. Markdown invites prose drift.

## End-of-session cleanup

At the end of every session, the agent must leave the environment in a state that the next session can pick up cleanly. "Clean state" means: no major bugs, code is orderly, the next agent can begin work on a new feature without first having to clean up an unrelated mess.

Concrete actions at session end:

- Commit progress to git with descriptive commit messages.
- Update `claude-progress.txt` with a note on what was done and what is next.
- Toggle the relevant feature's `passes` field only after end-to-end verification.
- Do not leave half-implemented features. If the session ran out of time, revert and note the partial work in progress.

This pattern uses git itself as memory. The next session reads the commit log to understand recent work, the same way a new human engineer would.

## Context resets versus compaction

Two strategies for keeping an agent productive across long tasks:

**Compaction**: the harness summarizes earlier parts of the conversation in place. Same agent, same session, just shorter history. Pros: continuity, no handoff cost. Cons: does not solve context anxiety; the agent still senses it is approaching a limit.

**Context resets**: the harness tears down the session entirely and rebuilds it from a structured handoff (the progress file, feature list, git history, init.sh). Fresh agent, fresh context. Pros: cures context anxiety, gives the agent a clean slate. Cons: adds orchestration cost, requires the handoff file to be complete.

When to use which:

- If the model exhibits context anxiety (Sonnet 4.5 did, Opus 4.6 mostly does not), use resets.
- If the model handles long contexts well, compaction is enough.
- For tasks that span days, resets are usually right regardless of model.

## The Ralph Wiggum loop

A simple variant of the reset pattern, popularized by Geoffrey Huntley in late 2025: a bash loop that feeds the same prompt repeatedly to a fresh agent context. State lives in files and git, not in the LLM's memory. When context fills, the agent rotates to a fresh session and reads state from disk.

The motto worth quoting once: "deterministically bad in an undeterministic world." Failures become predictable and recoverable.

A typical Ralph loop:

```text
Iteration 1, 2, 3, ... N:
  Fresh context window
  Read RALPH_TASK.md (the goal)
  Read .ralph/guardrails.md (lessons learned from previous failures)
  Read .ralph/progress.md (what is done)
  Work on next acceptance criterion
  Commit to git
  When context hits ~80% of max, ROTATE to fresh session
  Repeat until all acceptance criteria done
```

The "guardrails" file is the discipline that makes Ralph loops work. When something fails in iteration N, an entry is added with trigger, instruction, and the iteration where it was learned. Future iterations read guardrails first and avoid the trap.

When to use Ralph loops:

- Well-defined, test-driven tasks with machine-verifiable success criteria.
- Small to mid-sized projects.
- Contexts where you want unattended overnight work.

When to skip:

- Tasks requiring deep judgment or fuzzy success criteria.
- Tasks where most of the work is research or planning rather than implementation.
- High-stakes production code where two iterations of failure are fine but ten are not.

Variants of Ralph also support parallel loops (multiple agents in isolated git worktrees), each driving its own piece of the work.

## Multi-agent: planner / generator / evaluator

For tasks where self-evaluation is unreliable (UI design, complex full-stack apps), separate the agent that generates work from the agent that judges it. Anthropic's GAN-inspired three-agent pattern:

**Planner**: takes a 1-4 sentence user prompt and expands it into a detailed product spec. Stays at the product/architecture level; does not specify granular technical details (those propagate downstream errors). Asks for ambitious scope and weaves AI features into specs where appropriate.

**Generator**: implements the spec, working in sprints. One feature per sprint. Self-evaluates at the end of each sprint before handing off.

**Evaluator**: actively drives the running application using Playwright or DevTools. Tests UI interactions, API endpoints, database state. Grades each sprint against criteria with hard thresholds. Any criterion below threshold fails the sprint and triggers detailed feedback to the generator.

The non-obvious mechanic: before each sprint, the generator and evaluator negotiate a **sprint contract** in a shared file. They agree on what "done" looks like for that chunk of work before any code is written. The generator proposes; the evaluator reviews. They iterate until they agree, then build against the contract.

This pattern catches the failure mode where the generator and evaluator disagree on what was even being built. Writing down the done-condition before starting catches more scope drift than any prompt change.

## Why self-evaluation is unreliable

The empirical finding worth knowing: when an agent evaluates work it just produced, it tends to confidently praise the work even when, to a human observer, the quality is obviously mediocre. This is especially pronounced for subjective tasks like UI design but shows up on verifiable tasks too.

Separating generation from evaluation does not immediately fix this; the evaluator is still an LLM and is still inclined to be generous toward LLM outputs. But tuning a standalone evaluator to be skeptical is far more tractable than making the generator self-critical. Once external feedback exists, the generator has something concrete to iterate against.

## Making subjective quality gradable

For tasks where the success criterion is subjective (design quality, code review nuance, writing style), the planner/generator/evaluator pattern still works if you encode the criteria explicitly. Anthropic's frontend design example used four criteria with weights:

- **Design quality** (heavily weighted): does the design feel like a coherent whole rather than a collection of parts?
- **Originality** (heavily weighted): is there evidence of custom decisions rather than template defaults? Penalizes telltale AI patterns like purple gradients over white cards.
- **Craft**: technical execution. Typography, spacing, color, contrast. Most reasonable implementations pass by default.
- **Functionality**: usability independent of aesthetics.

The criteria are weighted to push the model toward aesthetic risk-taking. Each criterion has an example-based score breakdown that calibrates the evaluator. Few-shot examples reduce score drift across iterations.

The evaluator iterates: refine current direction if scores are trending well, pivot to a different approach if they are not.

## When to drop multi-agent components as models improve

The Anthropic team explicitly recommends re-examining the harness on every major model release. Specifically:

- The planner adds value as long as the model under-scopes when given raw prompts. Some models have improved enough that they spec well from a one-line prompt.
- The evaluator is load-bearing when the task sits at the edge of what the generator can do solo. As models improve, the evaluator becomes unnecessary overhead for tasks that used to need it.
- The sprint construct (one feature at a time with explicit handoffs) was needed for Sonnet 4.5. Opus 4.6 can often handle multi-feature work coherently in one sprint.

The methodical approach to simplification: remove one component at a time and review what impact it has on the final result. Cutting many at once obscures impact. Components that no longer earn their place should come out.

## QA-agent tuning takes work

The non-obvious finding: out of the box, Claude is a poor QA agent. In early runs Anthropic's evaluator would identify legitimate issues, then talk itself into deciding they were not a big deal and approve the work anyway. It also tested superficially.

The tuning loop:

1. Read the evaluator's logs.
2. Find examples where its judgment diverged from yours.
3. Update the QA prompt to solve for those issues.
4. Repeat.

It took several rounds before Anthropic's evaluator was grading reasonably. Plan for this iteration cost when adopting the pattern.

## Solo developer minimum

A solo developer probably does not need this whole apparatus. The minimum that earns its place:

- An `init.sh` that boots the project with one command.
- A short `progress.md` for any work spanning more than one session.
- Commit at the end of every session with descriptive messages.

Skip JSON feature lists, planner/generator/evaluator splits, and Ralph loops until the work is genuinely multi-day or unattended.
