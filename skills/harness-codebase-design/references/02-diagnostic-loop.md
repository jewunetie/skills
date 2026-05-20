# 02 The diagnostic loop

When an agent fails, the temptation is to retry, to switch models, or to write a longer prompt. Resist all three. Failures are signals.

## The diagnostic question

When something goes wrong, the load-bearing question is:

> What capability is missing, and how do we make it both legible and enforceable for the agent?

"Legible" means the agent can see and reason about the constraint while running. A rule that exists only in a Slack thread is invisible. A rule that exists in AGENTS.md is legible. A rule encoded in a custom lint with a remediation message is both legible and enforceable.

## Why "try harder" almost never works

OpenAI's report on five months of agent-only development is explicit: when something failed, the fix was almost never "try harder." Early progress was slow not because the agent was incapable, but because the environment was underspecified. The agent lacked tools, abstractions, or internal structure required to make progress on the goal.

Hashimoto's framing is the same from the solo-developer side: every time the agent does something bad, tune the environment. The environment is the guitar; the agent is the player.

## The four-step diagnostic loop

When the agent fails, walk through these in order:

1. **Identify the specific failure.** Not "the code was bad" but "it imported from the UI layer into the service layer," or "it marked the test as passing without running it," or "it reformatted the JSON state file." Specificity matters because the fix is specific.
2. **Locate where the constraint should live.** Five rough categories:
   - Knowledge the agent did not have. Lives in AGENTS.md, a doc, or a skill.
   - A capability the agent could not exercise. Lives in a tool, a CLI, or an MCP server.
   - A boundary the agent crossed. Lives in a custom lint or structural test.
   - A verification step the agent skipped. Lives in a hook or a back-pressure mechanism.
   - A pattern the agent kept replicating. Lives in a golden principle plus scheduled cleanup.
3. **Encode the fix.** Add the rule, write the lint, install the hook. Make the error message remediation-oriented so the agent can self-correct next time.
4. **Have the agent itself write the fix.** Per OpenAI's discipline: when the agent struggles, identify what is missing and feed it back into the repository, always by having the agent itself author the fix. This keeps the agent inside the workflow it is supposed to be living in.

## Where each kind of failure tends to belong

| Failure | Likely fix location | Reference |
|---|---|---|
| Wrong commands ("run the wrong test runner") | AGENTS.md | `references/03-knowledge-management.md` |
| Wrong APIs / outdated patterns | AGENTS.md or vendored reference docs | `references/03-knowledge-management.md` |
| Imports across architectural layers | Custom lint with remediation | `references/04-architectural-enforcement.md` |
| Reinvents existing utilities | Golden principle plus scheduled cleanup | `references/09-garbage-collection.md` |
| Marks features done without verification | Back-pressure hook on stop | `references/07-feedback-loops.md` |
| Floods context with passing test output | Silent-success / verbose-failure pattern | `references/07-feedback-loops.md` |
| Cannot see UI behavior | Browser tool (Chrome DevTools, Playwright MCP) | `references/05-application-legibility.md` |
| Cannot see logs or metrics | Observability access via standard query languages | `references/05-application-legibility.md` |
| Loses track on long tasks | Initializer / coding agent split, context resets | `references/08-long-running-coordination.md` |
| Skips QA, declares victory | Separate evaluator agent with hard thresholds | `references/08-long-running-coordination.md` |
| Probes data shapes blindly | Validate at boundaries, typed SDKs, golden principle | `references/04-architectural-enforcement.md` |
| Edits or removes tests | Strongly-worded AGENTS.md rule, plus pre-commit hook grep | `references/03-knowledge-management.md` |
| Disables a lint rule to make CI pass | Pre-commit hook that blocks lint config edits | `references/07-feedback-loops.md` |

## "Why is the same rule failing twice"

If a constraint is written somewhere and the agent is still violating it, the constraint has the wrong shape. Common reasons:

- It lives in a place the agent cannot see (Slack, a Notion page, a long AGENTS.md where it gets lost in the middle).
- The instruction is too soft. "Try to" is weaker than "must not." OpenAI uses strongly-worded behavioral constraints like "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
- It is documentation when it should be code. If the rule is mechanically checkable, promote it from doc to lint or hook. Documentation falls short over time; code does not.
- The error message does not teach the fix. A custom lint that says "rule violated" is less useful than one that says "Cannot import from `ui/components` in service layer. Move this logic to the service layer and pass results down as parameters. See docs/architecture/dependency-rules.md".

## The ratchet, not the brainstorm

The most important habit: only add constraints when you have seen a real failure (or a failure mode is near-certain at your scale). Brainstorming rules in the abstract is how AGENTS.md files get bloated and start hurting performance.

Every line of AGENTS.md, every custom lint, every hook should trace back to a specific past failure or a hard external constraint. If it does not, it is noise competing for the agent's attention budget.

The corollary: remove constraints when a more capable model makes them redundant. Re-examine the harness on every major model release. Components that no longer earn their place should come out.

## When the failure is the harness itself

Sometimes the agent fails because the harness is over-constrained, not under-constrained. Symptoms:

- The agent cannot complete legitimate tasks because a hook blocks them.
- Approval prompts come up so often that the human starts rubber-stamping.
- The agent visibly thrashes between two valid approaches because both are partially blocked.
- Iteration cycles take more than 5 minutes (the practical ceiling for keeping the agent productive).

When this happens, the fix is to relax or remove a constraint, not to add another one. Over-throttling is its own failure mode.
