# 05 Application legibility

For non-trivial work, the agent needs to see the running application, not just the source code. As code throughput rises, the bottleneck shifts from "writing code" to "verifying behavior." Anticipate this.

OpenAI's framing: make the application UI, logs, metrics, and traces directly legible to the agent. If the agent cannot observe a behavior, it cannot reliably build it.

## Bootable per worktree

The first prerequisite: each agent task gets an isolated, runnable instance of the app. OpenAI's pattern is "bootable per git worktree," where the application can be launched against any branch with a single command.

Concrete requirements:

- A single command (typically `init.sh` or `make dev`) starts the app and any dependencies (database, cache, queue) for the current worktree.
- The app's state is isolated: no shared dev database, no shared port. Different agent tasks do not collide.
- Startup is fast (10 to 60 seconds). If startup takes minutes, agents cannot iterate.
- Teardown is automatic. When the task ends, the environment goes away.

This pattern is the application equivalent of cattle, not pets. Stripe's "devboxes" are the strongest published example: pre-warmed EC2 instances that boot in 10 seconds, treated as disposable, identical to the environment human engineers use.

The Stripe insight worth internalizing: the agents use the same dev environment as humans. Every investment in developer experience is also an investment in agent capability. If the dev setup is painful for humans (slow CI, flaky tests, missing linters), it is worse for agents.

## UI access through Chrome DevTools or Playwright

Once the app boots, the agent needs to interact with the UI. The standard mechanisms are Chrome DevTools Protocol or Playwright (sometimes via Playwright MCP).

What this enables:

- Reproducing user-reported bugs by clicking through the path that triggered them.
- Validating that a fix actually fixes the bug, not just compiles.
- Reasoning about UI behavior directly (the agent can read the DOM, take screenshots, inspect network requests).

A typical UI-validation loop:

1. Select target, clear console.
2. Snapshot DOM and screenshots BEFORE the action.
3. Trigger the UI path (click, type, navigate).
4. Observe runtime events (console logs, network calls, errors) during interaction.
5. Snapshot DOM and screenshots AFTER.
6. Apply fix, restart, re-run validation.
7. Loop until clean.

This is the difference between "the code compiles" and "the feature actually works." Anthropic's Effective Harnesses paper found that without explicit prompting to use browser automation, Claude tended to test with unit tests and `curl` against APIs but missed end-to-end UI failures. Once given Puppeteer or Playwright MCP, performance improved dramatically.

A known limitation worth flagging: browser-native modals (alert, confirm) are not always visible to Puppeteer-style automation. Features that depend on these modals tend to be buggier as a result.

## Observability access

For server-side and performance work, the agent needs access to logs, metrics, and traces.

OpenAI's pattern is a per-worktree ephemeral observability stack. The agent works on a fully isolated app instance with its own logs and metrics that get torn down when the task completes.

Their stack architecture:

- App emits OpenTelemetry logs, metrics, and traces over HTTP.
- A local Vector instance fans data out to local storage.
- Storage is something queryable like Victoria Logs, Victoria Metrics, Victoria Traces.
- Each storage backend exposes a standard query API: LogQL, PromQL, TraceQL.
- The agent queries these APIs to correlate behavior with code changes.

The exact stack is not the point. The pattern is:

1. Use standard query languages (LogQL, PromQL, TraceQL) that are well represented in the agent's training data. Bespoke query languages mean the agent has to learn a new tool, which it does poorly.
2. Run the stack locally and ephemerally, not in shared infrastructure.
3. Make the agent's view match what a human operator would see.

Once observability is in-context, prompts become measurable. Examples that become tractable:

- "Ensure service startup completes in under 800ms."
- "No span in these four critical user journeys exceeds two seconds."
- "Identify the top three slowest database queries and propose indexes."
- "Find the request that triggered this error and trace it through all services."

These prompts would not work without the agent being able to query observability data directly.

## Sandboxes versus devboxes versus laptops

Three places agent code can run, in increasing order of isolation:

1. **The user's laptop.** Risky. A misbehaving agent can wipe files, exhaust disk, or hit production credentials cached in the shell. Acceptable only for solo developers with reflex-fast `Ctrl+C` and no production access from their dev machine.
2. **A local sandbox** (Docker container, VM, or ephemeral worktree). Better. The blast radius is contained. Agent-generated code runs in a known-clean environment with pre-installed runtimes and tools. Tear down between tasks. Suitable for small teams.
3. **A cloud devbox** (EC2 instance, Codespaces, or equivalent). Best for larger teams. Pre-warmed pools mean fast startup. Network-isolated from production. Each task gets its own. Stripe's "Hot and Ready" 10-second boot target is the high water mark.

A good sandbox ships with sensible defaults so the agent does not waste tokens setting up:

- Pre-installed language runtimes and major packages.
- Git, the test CLI, the build CLI, the linter.
- A headless browser (Chromium) for UI testing.
- Allowlisted network egress.
- No production credentials, no production database access.

## Same tools as humans

The Stripe corollary deserves restating: agents work best when they use the same tools as human engineers. Their agents run on the same devboxes humans use. They use the same linters, the same CI pipeline, the same rule files that Cursor and Claude Code users see.

The implication: stop building agent-specific infrastructure. Build great developer infrastructure. The agents benefit automatically.

This includes:

- The same test runners.
- The same database fixtures.
- The same authentication for internal services.
- The same logging and metrics dashboards.

Agent-specific shortcuts (mocking out the database, skipping auth, faking test fixtures) tend to hide failures that bite in production.

## Tool-output offloading

When the agent runs a command that produces a lot of output (a 2,000-line log file, a verbose test failure, a database export), do not let the full output flood the context window.

The pattern: the harness keeps a head and tail of the output above a token threshold and offloads the full output to the filesystem. The agent reads the full file on demand if the head and tail are insufficient.

This is closely related to the back-pressure pattern in `references/07-feedback-loops.md`. Every byte that enters the context window competes with the agent's reasoning. Bytes that do not directly inform the next action belong in a file.

## Solo developer minimum

A solo developer probably does not need a full observability stack on day one. The minimum:

- The app must be bootable with one command.
- Some way to see logs (just `tail -f` on a log file is fine).
- A typecheck and lint hook that runs after every change.
- For UI work, install Playwright MCP or use the Claude DevTools integration. The investment pays back fast.

Skip ephemeral observability stacks, devboxes, and Vector pipelines until the codebase is large enough that they earn their place.
