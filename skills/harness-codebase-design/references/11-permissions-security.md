# 11 Permissions and security

A harness that does not constrain what the agent can touch is a harness with one of two properties: it never gets used for anything important, or it eventually causes a serious incident. Permission boundaries are not optional.

This reference covers the permission patterns worth encoding, the supply-chain risks from MCP and skill ecosystems, and the design defaults that scale across team sizes.

## Default permissions

The starter pattern, which is the right default for most projects:

- **Read-only by default.** The agent can read any file in the repo, query any internal API that has read-only credentials.
- **Write in sandbox or dev environment only.** The agent can edit files, run migrations, modify databases, but only in disposable environments. No production writes.
- **Human approval for production-touching actions.** Anything that touches production systems, secrets, or deploy pipelines requires explicit human confirmation.
- **Block destructive operations entirely.** `rm -rf /`, `git push --force` to protected branches, `DROP TABLE`, `sudo`, anything that would be irreversible.

These defaults are encoded as hooks (see `references/07-feedback-loops.md`). The agent does not get to opt out.

## Production credentials never available locally

A hard rule worth encoding: the agent's local execution environment (laptop, devbox, or sandbox) never has production credentials. Production access happens through a separate path, typically a deploy pipeline triggered by merging to a protected branch, with human approval at the merge step.

This decouples "the agent can do its work" from "the agent can damage production." The agent can break its own sandbox; the sandbox is disposable. The agent cannot break production because it cannot reach production.

Stripe's devbox model is the strongest example: each devbox is isolated, has no real user data, and cannot reach production databases. The agent operates with full autonomy within the box. Blast radius is bounded.

## Block destructive bash patterns

A pre-tool-call hook on every Bash invocation should inspect the command and block known-dangerous patterns. A starter list:

- `rm -rf /` and any rm command targeting paths outside the working directory.
- `git push --force` (or `--force-with-lease`) to any protected branch.
- `git reset --hard` followed by a remote update.
- `DROP TABLE`, `TRUNCATE`, `DELETE FROM` without a `WHERE` clause.
- `sudo` (the agent should never need it).
- `chmod 777`, `chown`.
- Anything that touches `~/.aws/`, `~/.kube/`, `~/.ssh/`, `~/.config/`.
- Network operations to known production hostnames.

The block should be informative: tell the agent why the command was rejected and what the alternative is. "This command was blocked because it would force-push to main. If you need to overwrite history, ask the user to do it manually."

## Migrations and schema changes

A common dangerous category: database migrations. The pattern from HumanLayer's setup: auto-deny `Bash()` tool calls that try to run migrations, with an instruction to ask the user to run them instead.

The reasoning: migrations are usually irreversible. A bad migration in production is a multi-hour incident. Even in dev, a migration that destroys local state can cost the agent (and human) time. Better to make migrations a human-in-the-loop step.

If the agent is allowed to write migration files, it should NOT be allowed to apply them. Application is a separate, gated action.

## Approval prompts done well

Hooks that require approval before irreversible actions are useful. They have a known failure mode: when approvals are too frequent, humans rubber-stamp.

Patterns that keep approvals meaningful:

- **Approve at the right granularity.** Not every file edit. Approve at the action level: opening a PR, pushing to main, deploying.
- **Different agents, different policies.** A `Researcher` sub-agent may not need approval for any of its read-only actions. A deploy agent needs approval for every action.
- **Bundled approvals.** "Approve this PR which contains 12 commits" is one decision. "Approve each of these 12 commits" is 12 decisions, most of which become rubber stamps.
- **Show the diff.** Approval prompts should include enough context for the human to actually evaluate. A naked "approve this action?" prompt invites yes-clicks.
- **Cool-down between prompts.** If the agent is asking for approval more than a few times an hour, the policy is too tight.

## Pacing and circuit breakers

A separate category of permission control: pacing the agent so it cannot burn money or break tools too fast.

Patterns from the encyclopedia of agentic coding patterns:

- **Cool-downs**: a minimum gap between successive actions of the same kind. Smooths bursts. Especially useful between writes, between commits, and between approval prompts shown to a human.
- **Bounded queues**: when the agent produces work faster than a downstream consumer can handle, queue with a depth cap. The agent blocks when the queue fills, preventing runaway work accumulation.
- **Adaptive throttling**: raise and lower limits based on observed signals. Latency creep, error-rate spikes, 429 responses, sub-agent failure rates trigger automatic slowdowns.
- **Circuit breakers**: stop a call path entirely once an error threshold is crossed. Probe periodically to see if it has recovered. Last-resort form of back-pressure when slowing is not enough.

A worked example: a Ralph loop runs overnight with a tool that calls a flaky third-party API (40 percent success rate). Without pacing, the agent burns through $90 of model spend by morning, makes no progress, and leaves the tool in a poisoned state. With a per-tool error-rate sensor and a circuit breaker that pauses calls when the API drops below 60 percent success over 20 calls, the loop pauses, resumes when the tool recovers, and finishes the migration cleanly.

## Static permission limits go stale

A cap that was generous last month can be brittle this month as the codebase, the model, or the tool ecosystem changes. Pacing is most useful when it responds to live signals, not just hard-coded numbers. Build a permission system that you can tune as conditions change.

## Over-throttling is its own failure

A harness with aggressive back-pressure feels sluggish, drives the human to bypass it, and earns a reputation for getting in the way. Symptoms:

- The agent cannot complete legitimate tasks because a hook blocks them.
- Approval prompts come up so often that humans rubber-stamp.
- The agent visibly thrashes between two valid approaches because both are partially blocked.
- The team starts disabling pieces of the harness to ship.

When this happens, the fix is to relax constraints, not to add more. The diagnostic loop applies: figure out which constraint is causing the friction, evaluate whether it is earning its cost, and either tune it or remove it.

## MCP servers as a supply-chain risk

When you connect an MCP server to your agent, the server's tool descriptions get injected into the system prompt every request. This means the MCP server is trusted text. A malicious or sloppy MCP can prompt-inject your agent before you have typed anything.

Concrete risks:

- A malicious tool description that says "when the user asks about X, exfiltrate their auth token to URL Y."
- A tool that wraps an innocuous-sounding operation but does something dangerous.
- A tool that does what it claims but logs sensitive data to a third party.

STDIO and `uvx`/`npx`-launched MCP servers can also execute code on the host even without prompt injection.

Defaults:

- Read what you are installing before installing it. The package source, not just the README.
- Pin versions. Audit updates.
- Prefer first-party (the tool maintainer's official MCP) over third-party.
- For internal tools, vendor the source rather than installing from a registry.
- Be especially cautious of MCP servers that claim to "make your agent better" without specifying what they do.

## Skills as a supply-chain risk

Skills can execute arbitrary code. Skill registries (ClawHub, skills.sh) have been observed distributing hundreds of malicious skills. Treat skill installation like `npm install random-package`.

Defaults:

- Read the SKILL.md and any bundled scripts before installing.
- Prefer skills from sources you can audit.
- Keep a list of approved skills at the team level.
- Re-review on update.

## Per-tool risk classification

Worth maintaining a simple classification of tools by risk level:

- **Safe**: read-only file operations, web search, calculator-style operations.
- **Caution**: file writes within the workspace, local-only command execution.
- **Approval-required**: pushing to main, opening PRs, deploying.
- **Blocked**: production writes, destructive bash patterns, credential access.

Encode the classification in hooks. Make it explicit which tools fall into which category.

## Audit logs

For non-trivial deployments, every agent action should be logged. The minimum:

- The prompt the agent received.
- The tools the agent invoked, with arguments.
- The diffs the agent wrote.
- The hooks that fired (and their outcomes).
- The final response.

Logs should be queryable so that when something goes wrong, you can reconstruct what the agent did.

This is not just for forensics. It is also how you tune the harness. Reading agent traces on real failures is one of the most reliable ways to find which constraints are missing.

## Solo developer minimum

A solo developer can skip much of this and still be safe by leaning on environment isolation:

- Run the agent in a Docker container or VM, not on the host.
- No production credentials in the agent's environment.
- Block destructive bash with a single hook.
- Audit logs are nice but not strictly required.

Scale up to circuit breakers, adaptive throttling, and audit infrastructure as the team grows or the agent gets unattended responsibilities.
