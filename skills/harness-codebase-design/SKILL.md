---
name: harness-codebase-design
description: Design a codebase to work well with AI coding agents (Claude Code, Codex, Cursor, Aider). Use this skill when the user is starting or retrofitting a repository for agents, asking what AGENTS.md or CLAUDE.md should contain, designing project structure for AI assistance, asking about harness engineering, saying an agent keeps making the same mistake, asking how to make agents reliable on long-running tasks, or trying to make their codebase legible to coding agents. Trigger on indirect phrasings too. Examples include "set up my project for Claude Code", "make my repo agent-friendly", "stop my agent from doing X", "best architecture for AI-generated code", or "the agent keeps reinventing utilities". Use proactively when the user describes building a project with agent assistance and has not yet thought about scaffolding, AGENTS.md, custom linters, hooks, or feedback loops.
---

# Harness engineering for codebase design

This skill helps users design (or retrofit) a codebase so coding agents can work in it reliably. The unifying mantra, from Mitchell Hashimoto: anytime an agent makes a mistake, engineer a fix into the environment so it cannot make that mistake again. The job is to design environments, specify intent, and build feedback loops, not to write code by hand.

This file is a table of contents. The depth lives in `references/`. Read only the references you need for the current question.

## How to use this skill

1. Diagnose the user's situation with the questions below. Do not ask all of them; ask only the ones the conversation has not already answered.
2. Map them to a scale tier: solo developer, small team (2 to 10), or larger team or organization.
3. Walk through the load-bearing decisions in order, pulling from the relevant references.
4. Offer to scaffold concrete artifacts (AGENTS.md, docs tree, golden principles file, hooks) from `templates/` when the user is ready.
5. Stop when the user has enough to act on. Do not produce every reference at once.

## Diagnostic questions

Ask only what is missing from the conversation so far. Use the `ask_user_input_v0` tool when present; otherwise ask inline.

1. Project stage: starting a new repo, or retrofitting an existing one.
2. Team size and audience: solo, small team, or larger organization.
3. Primary agent: Claude Code, Codex, Cursor, OpenCode, Aider, or other.
4. Primary language and stack (only if it matters for the question being asked).

If the user gave a specific failure ("the agent keeps doing X"), skip diagnosis and go straight to `references/02-diagnostic-loop.md`.

## Scale tiers

Different patterns are load-bearing at different scales. Tag every recommendation by tier so the user does not over-build.

- **Solo developer**: AGENTS.md, a small docs tree, hooks for typecheck and lint, the diagnostic loop, basic back-pressure. Skip multi-agent patterns and scheduled cleanup agents.
- **Small team (2 to 10)**: add architectural enforcement via custom linters or structural tests, the docs system of record, sub-agents for context control, light golden principles.
- **Larger team or organization**: add scheduled garbage collection, multi-agent planner/generator/evaluator patterns where evaluation is hard, devbox-style sandboxes, throughput-aware merge philosophy, harness-as-template across repos.

## What to consult when

| User question or signal | Read this reference |
|---|---|
| "Where do I start" / "what is harness engineering" | `references/01-mental-model.md` |
| "The agent keeps doing X wrong" | `references/02-diagnostic-loop.md` |
| "What should AGENTS.md contain" / "is my CLAUDE.md good" | `references/03-knowledge-management.md` |
| "How should I structure docs" / "where does spec live" | `references/03-knowledge-management.md` |
| "How do I keep the agent from breaking architecture" | `references/04-architectural-enforcement.md` |
| "What should I lint" / "what taste rules to encode" | `references/04-architectural-enforcement.md` |
| "How does the agent see my running app" / "logs and UI" | `references/05-application-legibility.md` |
| "Should I install MCP X" / "too many tools" | `references/06-tools-skills-subagents.md` |
| "What are skills for" / "progressive disclosure" | `references/06-tools-skills-subagents.md` |
| "Should I use sub-agents" / "frontend engineer agent" | `references/06-tools-skills-subagents.md` |
| "Hooks" / "pre-commit" / "verification on stop" | `references/07-feedback-loops.md` |
| "Tests flooding context" / "back-pressure" | `references/07-feedback-loops.md` |
| "Multi-hour tasks" / "context resets" / "Ralph loop" | `references/08-long-running-coordination.md` |
| "Planner / generator / evaluator" / "GAN-style harness" | `references/08-long-running-coordination.md` |
| "Codebase drift" / "AI slop accumulating" / "cleanup PRs" | `references/09-garbage-collection.md` |
| "Should I block on flaky tests" / "merge gates at agent throughput" | `references/10-throughput-and-merge.md` |
| "What permissions should the agent have" / "MCP risks" | `references/11-permissions-security.md` |
| "What did not work for other teams" / "common mistakes" | `references/12-antipatterns-and-tiers.md` |

## Templates available for scaffolding

When the user wants concrete starter files, offer these:

- `templates/AGENTS.md.template`: table-of-contents-style entry file under 100 lines.
- `templates/docs-tree-skeleton.md`: directory layout and stub files for the docs system of record.
- `templates/golden-principles.md.template`: opinionated mechanical rules to enforce continuously.
- `templates/taste-invariants-starter.md`: a starter list of static checks worth encoding as custom lints.
- `templates/back-pressure-hook.sh.template`: a verification hook with silent-success, verbose-failure semantics.

Do not output every template at once. Ask which ones the user wants.

## Operating principles for this skill

- **Earn each rule.** Do not recommend a constraint unless the user has actually hit the failure it prevents, or the failure is near-certain at their scale. Hashimoto's discipline: every line of AGENTS.md should trace back to a specific past failure.
- **Recommend by scale.** Tag every recommendation with the tier where it pays off. Solo developers do not need scheduled cleanup agents; large teams cannot survive without them.
- **Prefer paraphrase over jargon.** Most users are not in the harness-engineering literature. Explain terms briefly when introducing them.
- **Surface aspirational states honestly.** End-to-end autonomous feature loops, six-hour single runs, full agent-generated million-line codebases all exist, but they depend on harness investment most users have not made. State this when the user asks.
- **The skill is meta-eating-its-own-dogfood.** This SKILL.md is short and routes to references because that is exactly the pattern being taught.

## Open questions to flag for the user

When recommending patterns drawn from the broader literature, be honest about what is still being learned:

- Architectural coherence over years in fully agent-generated systems is unproven.
- The right division of labor between human judgment and encoded rules is still an active question.
- Patterns evolve as models improve. A component that was load-bearing for Sonnet 4.5 (context resets to combat context anxiety) may be unnecessary for Opus 4.6. Re-examine the harness when models change.
