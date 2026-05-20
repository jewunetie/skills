# 01 Mental model

## What harness engineering is

Mitchell Hashimoto coined the working definition in February 2026: harness engineering is the practice of taking every observed agent mistake and engineering a permanent fix into the environment, so the agent cannot make that mistake again.

A useful equation, from Viv Trivedy:

```text
Agent = Model + Harness
```

The model is the language model. The harness is everything else: system prompts, AGENTS.md or CLAUDE.md, tools, MCP servers, sub-agents, hooks, sandboxes, observability, feedback loops, recovery paths. Two products with the same underlying model but different harnesses produce dramatically different results. On Terminal Bench 2.0, the same Opus 4.6 model jumped from rank 33 in Claude Code to rank 5 in a custom harness, with no change to the model.

## What changes when agents do most of the writing

Three things shift:

1. The engineer's primary job moves from writing code to designing environments, specifying intent, and building feedback loops.
2. Human time and attention becomes the scarce resource. Every harness decision is a tradeoff that protects it.
3. The discipline of software engineering moves from the code into the scaffolding around it. Tooling, abstractions, and invariants become the load-bearing surface.

## Two halves of the work

Harness engineering has two halves that are not sequential:

- **Build the environment**: AGENTS.md, docs structure, custom linters, hooks, sandboxes, observability, golden principles.
- **Manage agents within it**: prompts, sub-agent orchestration, review workflows, when to escalate to a human.

Each half informs the other. Agent failures tell you what the environment is missing. A better environment lets you manage with less friction.

## Two kinds of harness components

Birgitta Boeckeler's framing is useful: harness components fall into two categories.

- **Guides** (feedforward): rules, types, AGENTS.md content, context provided up front, architectural constraints, naming conventions. They steer the agent before it acts.
- **Sensors** (feedback): tests, linters, evaluators, observability, output parsers, evals. They catch mistakes after the agent acts.

Both can be computational (deterministic) or inferential (LLM-based). Both are needed. Guides without sensors miss what the rules did not anticipate. Sensors without guides drown in preventable failures.

## The behavior-first design heuristic

When designing a new harness component, name the behavior you want, then derive the component that delivers it. If you cannot name the behavior a component exists for, the component should not exist.

Examples of behaviors and the components they motivate:

- "Work durably across sessions" requires a filesystem and git.
- "Execute arbitrary actions safely" requires a sandbox.
- "Survive long tasks without context overflow" requires compaction, tool-output offloading, sub-agents, or context resets.
- "Catch broken UI without me noticing" requires Playwright or DevTools access plus an evaluator.
- "Stop the agent from disabling tests when they fail" requires a hook that blocks the diff.

This heuristic is the antidote to cargo-cult harness building.

## What harnesses are not

Harnesses are not:

- A magic config file you set up once. A harness is a living system that ratchets every time the agent fails in a new way.
- Equivalent to prompt engineering. Prompt engineering optimizes a single exchange. Context engineering manages what the model sees per call. Harness engineering designs the entire execution environment around an autonomous agent.
- A substitute for clear thinking about what the project is. The harness amplifies whatever direction you give it. Bad direction with a great harness gets you bad code very quickly.

## How harnesses evolve as models improve

A common misconception is that better models will obviate harnesses. Anthropic's framing is more accurate: harnesses do not shrink, they move.

Every harness component encodes an assumption about what the model cannot do on its own. When the model gets better at something, that component becomes load-bearing for nothing and should come out. When the model unlocks something new, the ceiling moves outward and new scaffolding is needed to reach it.

Concrete example: Claude Sonnet 4.5 exhibited "context anxiety" (wrapping up work prematurely as the window filled). The standard mitigation was full context resets between sessions. Opus 4.6 largely removed that behavior on its own, so context-reset scaffolding became dead code in many harnesses. In its place, longer autonomous runs became viable, which required different scaffolding (better progress tracking, more rigorous evaluators).

The implication: re-examine the harness whenever a major model release lands. Strip away components that are no longer load-bearing. Add components that target the new ceiling.

## Why harness work compounds

Every AGENTS.md update prevents a class of future failures. Every custom linter teaches every future agent session. Every tool exposed via the right interface makes every subsequent task faster. The upfront cost is real, but the returns accelerate. This is why the discipline is worth investing in even when it feels like overhead in the short term.

The companion to this: every component you add that does not earn its place dilutes the rest. Ratchet rules in based on observed failures. Resist the urge to brainstorm constraints in the abstract.

## Why this matters even for solo developers

Most of the public examples (OpenAI's million-line codebase, Stripe's Minions writing 1,300 PRs a week, Anthropic's three-agent harness) are at organizational scale. The mental model still applies at solo scale, but the implementation is much lighter. A solo developer needs:

- A short AGENTS.md or CLAUDE.md (under 100 lines, often under 60).
- Hooks for typecheck and lint that surface errors back to the agent.
- A diagnostic discipline: when the agent does something dumb, fix the environment, do not just retry.
- Back-pressure that does not flood context.

That is enough to see most of the gains. Larger teams add scheduled cleanup, multi-agent patterns, devbox sandboxes, and so on.
