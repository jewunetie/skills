# 07 Feedback loops: hooks and back-pressure

The single highest-leverage investment after AGENTS.md, and the one most teams underdo. Verification mechanisms that the agent can use to check its own work are what separate "the agent ran for an hour" from "the agent shipped working code."

The HumanLayer team is direct on this: back-pressure is one of the highest-leverage things they have spent time on. Hashimoto, from the solo-developer side: if you give an agent a way to verify its work, it more often than not fixes its own mistakes and prevents regressions.

## Hooks: enforcement, not advice

Hooks are scripts that run automatically at lifecycle points: before a tool call, after a file edit, on session stop, before commit, on session start. They are conceptually similar to git hooks but apply to the agent's loop, not the developer's.

The distinction worth internalizing: hooks separate "I told the agent to do X" from "the system enforces X." Anything in AGENTS.md is a request the agent may or may not honor on the 47th iteration of a debugging session. Anything in a hook always happens.

What different harnesses support:

- **Claude Code**: hooks. Documented at `code.claude.com/docs/en/hooks`. Quite flexible.
- **OpenCode**: plugins, similar capability.
- **Codex**: no equivalent at the time of writing. Plan around this.
- **Cursor**: limited equivalent through workflow rules.

## Common hook use cases

The patterns worth knowing, ordered roughly by leverage:

**Verification on stop**: when the agent thinks it is done, run typecheck, lint, build, and a relevant subset of tests. If any fail, the failures get surfaced back to the agent and it is forced to keep working until they resolve. This is the highest-leverage hook by a wide margin.

**Block destructive bash**: a hook on every Bash tool call inspects the command. Patterns to block include `rm -rf /`, `git push --force` to protected branches, `DROP TABLE`, `sudo`, anything that touches production credentials. Block silently or with a polite message ("ask the user to run this manually").

**Auto-deny dangerous tool calls**: HumanLayer auto-denies `Bash()` tool calls that try to run database migrations, with an instruction to ask the user instead.

**Approval prompts for irreversible actions**: require explicit approval before opening a PR, pushing to `main`, deploying, or merging. Important caveat: too many approval prompts cause humans to rubber-stamp, which is worse than no approvals.

**Auto-format on write**: a post-write hook runs the project formatter. The agent does not waste tokens on whitespace.

**Slack or system notifications**: when the agent finishes or hits a long-blocked state, send a notification. Useful for parallel agent workflows.

**Pre-commit lint and quick test pass**: before any commit, run a fast subset of checks. If they fail, surface to the agent, do not let the commit complete.

**Lint config protection**: a pre-commit hook that blocks edits to lint config files prevents the failure mode of "agent disables a rule to make CI pass." This pattern shows up in the literature often enough to be worth encoding.

## Silent success, verbose failure

The single most important shape of every verification hook:

> If the check passes, the agent hears nothing. If it fails, the full error gets injected back into the agent's loop.

The HumanLayer formulation:

```bash
run_silent() {
  output=$("$@" 2>&1)
  if [ $? -eq 0 ]; then
    echo "✓"
  else
    echo "$output"
  fi
}
```

Why this matters. Imagine a typecheck that runs on every file write. Without this pattern, every successful typecheck dumps "TypeScript: 0 errors" plus 50 lines of dependency resolution noise into the agent's context. After an hour of work, the agent's context is 80 percent typecheck output and 20 percent task-relevant code. The agent's reasoning degrades. It starts to lose track.

With the pattern, successful typechecks contribute one character ("✓") to context. Failed typechecks contribute the full actionable error. The signal-to-noise ratio is preserved.

## Filter test output ruthlessly

Tests are the most common context-flooding offender. The default output of any test framework is too verbose for an agent.

Standard patterns:

- **Use `--bail` / `pytest -x` / `go test -failfast`**: stop on first failure. The agent fixes one thing, runs again, picks up the next failure. This avoids the agent context-switching between five different bugs simultaneously.
- **Strip generic stack frames** that do not point at user code.
- **Strip timing information** unless the test is actually a performance check.
- **Use grep, sed, awk** to extract just the assertion that failed. Most assertion libraries print structured output that is parseable.
- **Framework-specific parsers**: extract test counts (passed, failed, skipped) from pytest, jest, go test, vitest, etc. So the agent has visibility into "23 tests passed, 1 failed" without seeing 22 success lines.

This is more work than just letting the test runner spew, and it pays back many times over in context efficiency.

## The iteration cycle latency rule

A practical heuristic from Khare's "Why your AI agent keeps failing":

- Edit-build-test-feedback under 2 minutes: good range for autonomous work.
- 2 to 5 minutes: tolerable, agent will iterate slowly.
- Over 5 minutes: too slow; agent and human both lose patience.
- Under 30 seconds: check that tests are actually catching issues, not rubber-stamping.

If the iteration cycle is too slow, the fix is on the test infrastructure side: parallelize tests, run only the relevant subset, cache build artifacts, use file-watch incremental builds.

## Back-pressure beyond code

The same principle extends past code-correctness checks:

- **Context back-pressure**: drop low-signal context (large tool outputs, repeated reads of the same file) before it reaches the model. Tool-call offloading is the standard implementation.
- **Permission back-pressure**: constrain what the agent can touch. Read-only by default, write only in sandbox/dev, human approval for production. See `references/11-permissions-security.md`.
- **Pacing back-pressure**: cap edits per minute or commits per session for runaway-prevention. Especially useful for long-running agent loops where a flaky tool can burn money fast.
- **LLM-as-judge back-pressure** for non-mechanical checks. Creative quality, UX feel, code review concerns that resist programmatic evaluation. Use a separate evaluator agent that returns binary pass/fail; accept eventual consistency through iteration.

## Strongly typed languages amplify hook leverage

A strong type system is itself a form of back-pressure. When the agent generates code in a language with an effective type system (TypeScript strict mode, Rust, Go, Kotlin, Swift), the compiler catches entire categories of errors instantly. Wrong types, missing fields, impossible states all surface immediately. The agent gets feedback in seconds instead of minutes.

This is partly why typed languages have been growing in popularity for agent-assisted development. It is not just that typed languages produce better code in general; the feedback signal is faster and more actionable.

If the project is already in a dynamically typed language, adding gradual typing (type hints in Python, JSDoc in JavaScript, mypy or Sorbet in production) tightens the feedback loop substantially.

## The CI loop, capped

For unattended agent workflows that push to CI, cap the retry loop. Stripe's pattern, which is worth borrowing:

1. Local checks run first ("shift feedback left"). Lint with autofix runs in under one second via cached heuristics for which rules apply. Local linting under five seconds.
2. Only after local checks pass does the agent push to CI.
3. CI runs a relevant test subset (Stripe runs a subset of their 3 million tests).
4. If CI fails, the agent gets one more attempt. Read the logs, fix locally, push again.
5. If the second attempt fails, the PR is handed to a human. No infinite retry.

The two-attempt cap balances the magic of autonomous iteration with the real costs of compute. Letting the loop run indefinitely is a token-burning trap.

## When CI is too slow

A common failure mode: the agent pushes to CI, waits 8 minutes, sees a typecheck error that should have been caught locally. The fix is "shift feedback left." Anything that can be checked locally in under 5 seconds belongs in a pre-push hook, not in CI.

This includes lint, typecheck, formatting, and (where possible) a fast smoke test. Heavy integration tests still belong in CI.

## Self-verification through evaluators

For tasks where a binary pass/fail is hard (UI quality, code review nuance), a separate evaluator agent works as back-pressure. See `references/08-long-running-coordination.md` for the planner/generator/evaluator pattern. The key insight: agents skew positive when grading their own work, so evaluation needs to be a separate agent (or a separate prompted role with no memory of generation).

## Solo developer minimum

A solo developer should set up, in this order:

1. A typecheck hook on session stop that surfaces type errors back to the agent.
2. A lint hook on session stop that surfaces lint errors.
3. The silent-success / verbose-failure pattern for both.
4. A pre-commit hook that blocks edits to test files unless explicitly authorized.

That is enough to capture most of the leverage. Add destructive-command blocking once the agent has tried something dangerous. Add slack notifications and approval flows only if you are running unattended.
