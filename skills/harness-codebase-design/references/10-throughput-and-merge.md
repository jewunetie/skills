# 10 Throughput-aware merge philosophy

When the agent throughput rises, several conventional engineering norms become counterproductive. This is one of the more counterintuitive lessons in the literature, and getting it wrong stalls otherwise-functional harness setups.

OpenAI's framing: "In a system where agent throughput far exceeds human attention, corrections are cheap and waiting is expensive."

## When norms flip

The norms that stop working at high agent throughput, and what to replace them with:

| Conventional norm | At agent throughput | Replacement |
|---|---|---|
| Block on flaky tests | Causes constant manual intervention | Address with retries; investigate flakiness async |
| Long-lived feature branches | Branches diverge from main faster than humans can reconcile | Short-lived PRs, one feature each |
| Multiple rounds of human review per PR | Becomes the bottleneck | Agent-to-agent review with humans on selected PRs only |
| Comprehensive test runs on every PR | CI minutes balloon | Selective subset relevant to the change |
| "Let CI catch it" | Wastes minutes per iteration | Shift feedback left to local checks under 5 seconds |
| Code freeze before release | Stops the agent fleet entirely | Continuous deployment with feature flags |
| One PR per feature | Sometimes too coarse | One PR per small, mergeable increment |

These flips are real but scale-dependent. They make sense at agent throughput. They are irresponsible at low throughput. The skill should explicitly flag this.

## Minimal blocking merge gates

The philosophy: PR gates should be the minimum required to keep main shippable. Anything more becomes friction the agent (and the team) routes around.

What stays as a hard block:

- Type errors.
- Lint failures (with autofix not applied).
- Security-scan critical findings.
- Breakage of a relevant subset of tests.
- Failed end-to-end smoke test on the merge candidate.

What does NOT stay as a hard block:

- Flaky test failures (retry; investigate the test async).
- Style nits the linter did not catch (let the cleanup agent fix later).
- Coverage decreases below a threshold (track but do not block).
- Non-critical security-scan findings (track and triage, do not block).
- Documentation lag (a doc-gardening agent will catch up).

The line between blocking and non-blocking should be calibrated to: "would I rather wait an hour for this to pass, or merge and let a small follow-up PR fix it." If the latter, do not block.

## Test flakes: retry, do not investigate at merge time

A test that fails intermittently is not a reason to block a merge that has nothing to do with the failing test. The default response should be a retry. If the same flake fires repeatedly, it goes into a queue for async investigation.

The mechanism that makes this safe: track flake rates per test, surface them in a dashboard, and have a scheduled cleanup agent (or a rotation of humans) work the backlog. Flakes do not get to hold up unrelated work.

This works only if you have decent flake detection. If your CI cannot tell the difference between a flake and a real failure, fix that first.

## Short-lived PRs

Long-lived branches are agent-hostile. Each day a branch lives is another day it diverges from main. Rebase conflicts cost agent and human time. The agent has to re-validate work that was already validated. CI runs duplicate effort.

The pattern: PRs open, get reviewed (by agents and selectively by humans), and merge within hours, not days. If a feature is too big for that, decompose into small mergeable increments using feature flags to hide the in-progress feature from users.

This is the same one-feature-at-a-time pattern from `references/08-long-running-coordination.md`, applied to PRs rather than agent sessions.

## Agent-to-agent review

At agent throughput, every PR getting human review is the bottleneck. The replacement, from OpenAI's discipline:

- The agent that wrote the PR reviews its own changes locally first.
- The agent then requests additional agent reviews (locally or via CI).
- The agent responds to review feedback and iterates until all reviewers are satisfied.
- Humans review selectively, focused on the PRs that matter (load-bearing changes, security-relevant changes, anything outside the agent's normal sandbox).

This is the "Ralph Wiggum loop" pattern applied to review: the agent iterates against feedback until the loop closes.

The non-obvious requirement: this only works if agent reviewers are tuned. Out of the box, agent reviewers are too generous. They need iteration to become useful (see `references/08-long-running-coordination.md` on QA-agent tuning).

## The two-attempt cap on CI loops

For unattended agent workflows that push to CI, cap the loop. Stripe's pattern:

1. Local checks run first (lint with autofix, typecheck, fast smoke tests).
2. The agent pushes to CI only after local checks pass.
3. CI runs a relevant test subset.
4. If CI fails, the agent gets one more attempt: read the logs, fix locally, push again.
5. If the second attempt fails, the PR is handed to a human. No infinite retry.

The cap balances autonomy against compute cost. Letting the loop run indefinitely is a token-burning trap, and the diminishing returns past two attempts are real.

## Shift feedback left

The shape of fast feedback at high throughput: anything that can be checked locally in under five seconds belongs in a pre-push hook, not in CI.

This includes:

- Lint with autofix.
- Type check.
- Format check.
- Quick smoke tests.
- Conventional commit message check.

Heavy integration tests still run in CI. But the cheap, deterministic checks happen locally so the agent (and humans) get feedback in seconds.

Stripe's implementation: a background daemon precomputes and caches heuristics for which lint rules apply to which paths, so lint runs in under one second even on a large codebase. Local linting under five seconds. This means the first CI pass usually succeeds.

## Test selection over comprehensive runs

Running the entire test suite on every PR is fine when the suite is small and humans are the bottleneck. At agent throughput on a large suite, it is wasteful. The pattern:

- Map test dependencies to source files.
- For each PR, run only the tests that depend on the changed files (and a small randomized subset of unrelated tests for safety).
- Run the full suite on a schedule (nightly) and on release candidates.

Tools: most modern test runners support this pattern. For Python, `pytest-testmon` or path-based selection. For JavaScript, Jest's `--findRelatedTests`. For larger codebases, custom mappings based on the dependency graph.

## When humans should review

Humans review selectively, focused on:

- Changes to load-bearing infrastructure (CI, deploy scripts, security-relevant code).
- Changes that cross architectural domains.
- Changes to the harness itself (AGENTS.md, custom lints, hooks).
- Changes that the agent flagged as uncertain or that triggered escalation.
- Changes that touch external interfaces (API contracts, database migrations).
- A random sample of routine PRs as a sanity check.

What humans should not review (let agent review handle it):

- Routine bug fixes that do not cross domain boundaries.
- Test additions.
- Documentation updates.
- Refactors that are mechanically validated.
- Cleanup PRs from scheduled agents.

## The "everything is shippable" target

The end-state these patterns push toward: main is always shippable. Every PR that lands is small, reviewed, tested, and feature-flagged if needed. Releases happen on a schedule (or continuously) without code freezes.

This is the same target good engineering teams have always pursued. Agent throughput just makes it more important: a code freeze that stops the agent fleet for a week is an enormous waste.

## When this advice does NOT apply

The throughput-aware norms above are for codebases where agents are doing the bulk of the writing. Specifically:

- If most code is still hand-written by humans, the original norms still apply. Long-lived branches are tolerable. Comprehensive review is feasible.
- If the team is small enough that humans review every PR anyway, agent-to-agent review adds friction without reducing the bottleneck.
- If the codebase has high blast-radius failure modes (financial, medical, safety-critical), conservative gating is worth the cost.

The skill should ask the user about scale and risk profile before recommending these flips.

## Solo developer minimum

A solo developer with a single agent loop can adopt much of this without the team-coordination overhead:

- Short-lived PRs by default. Local checks before push.
- The two-attempt cap on CI loops.
- Selective test runs on the change.
- Skip agent-to-agent review (it is just you reviewing).

Skip the "everything is shippable" continuous deployment pattern unless you actually need it. For most solo projects, manual deploys are fine.
