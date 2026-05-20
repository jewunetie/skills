# 12 Antipatterns and scale-tier guidance

What does not work, drawn from the public failure stories of teams that have done this seriously. Plus a clearer mapping of which patterns earn their place at which scale.

## Antipatterns to call out explicitly

These come up enough in the literature that the skill should warn against them when relevant.

### Designing the ideal harness upfront

The most common antipattern, especially among engineers used to upfront design. The temptation is to think through every failure mode the agent might have, write rules for all of them, and ship a complete harness on day one.

What actually happens: you anticipate the wrong failures. The agent fails in ways your rules do not cover, while your rules block legitimate work. The team disables pieces of the harness to ship. The harness becomes a graveyard of stale rules nobody trusts.

The fix: ratchet, do not brainstorm. Add constraints when you have observed real failures, not when you imagine future ones. Hashimoto's discipline applies: every line of AGENTS.md should trace back to a specific past failure.

### Auto-generating AGENTS.md

The ETH Zurich study tested 138 agentfiles and found that LLM-generated agentfiles actively hurt resolution rates while costing 20 percent more tokens. They are filled with plausible-sounding but mostly useless instructions.

The fix: write AGENTS.md by hand. If you must use an agent, have it propose lines based on observed failures and pick the ones that map to real failures.

### Stuffing the system prompt with everything important

A long AGENTS.md, plus a long set of tool descriptions, plus a long set of skill files all auto-loaded, plus the agent's own working context. By the time the agent starts working, half the context window is gone and the agent is already in the "dumb zone."

The fix: progressive disclosure. AGENTS.md as a table of contents, not an encyclopedia. Skills load on demand. Tool descriptions get pruned. Sub-agents firewall off intermediate noise.

### Installing MCP servers and skills "just in case"

The instinct to install every popular tool and skill once you discover the harness ecosystem. The result is a ballooning system prompt full of tool descriptions for things the agent never uses, and a security surface with many third-party dependencies.

The fix: install only what solves a specific failure or unlocks a specific capability. Turn off MCP servers you are not actively using. Read what you install.

### Running the entire test suite at the end of every agent session

A test suite that takes 5 minutes to run becomes the bottleneck. The agent finishes work, the suite runs, the agent waits, the agent moves to the next task with stale context. Multiply by many agent sessions and you are paying for compute, time, and context window with no commensurate quality gain.

The fix: run a relevant subset on session stop. Map test dependencies to source files. Run the full suite on a schedule (nightly) and on release candidates only.

### Micro-optimizing per-sub-agent tool access

A tempting-looking optimization: set up sub-agents with carefully limited tool sets, hoping that "the frontend agent does not need bash" produces better outcomes. HumanLayer tried this. It did not work.

What actually happens: the sub-agents thrash. Tools that turn out to be needed are missing. The team spends time on configuration that does not improve outcomes.

The fix: most coding-agent harnesses do not have a robust configuration surface for per-sub-agent tool restriction anyway. Use sub-agents for context control and cost control, not for capability fencing. If you actually need a fenced tool surface, use a separate agent harness with its own tool config.

### Using sub-agents for role specialization

The "frontend engineer," "backend engineer," "data analyst" sub-agent pattern. It feels intuitive but does not work. Sub-agents that try to be subject-matter specialists end up doing weird things because the orchestrator has to write detailed prompts to fence in their behavior, and the orchestrator is doing exactly the work the sub-agent was supposed to do.

The fix: use sub-agents as context firewalls. Dispatch a sub-agent with one specific task that takes many tool calls and has a short answer. Get the answer back. The parent decides what to do with it.

### Letting the CI loop run forever

The agent pushes to CI. CI fails. The agent reads the logs, fixes locally, pushes again. CI fails. The agent fixes. CI fails. Loop continues until you wake up to a $200 cloud bill and no progress.

The fix: cap the loop at two attempts. After the second failure, hand the PR to a human. Stripe's pattern. The diminishing returns past attempt two are real.

### Overwhelming the human with approvals

A harness that requires human approval for every meaningful action seems safer than one that does not. In practice, when approvals come up too often, humans rubber-stamp. The signal becomes noise.

The fix: approve at the right granularity. Bundle related actions. Show the diff. Save approval for things that genuinely need human judgment.

### Believing harnesses are obsolete because the model got better

The "wait for GPT-7" or "wait for Opus 5" mindset. It is true that better models reduce the need for some scaffolding. It is also true that better models unlock new ceilings that need new scaffolding to reach. Harnesses do not shrink; they move.

The fix: re-examine the harness on every major model release. Strip components that are no longer load-bearing. Add components that target the new ceiling.

### Treating the harness as a config file

A harness is a living system. It changes as failures surface, as the codebase grows, as the team scales, as models improve. Treating it as set-and-forget is the same mistake as treating a CI pipeline as set-and-forget.

The fix: review the harness on a regular cadence. Read recent agent traces. Find places where the harness is over-constrained or under-constrained. Tune.

## What did work for teams shipping at scale

The flip side of the antipatterns. Patterns that show up consistently across HumanLayer, OpenAI, Anthropic, and Stripe:

- **Start simple.** Add configuration only when the agent actually fails.
- **Iterate openly.** Design, test, throw away, repeat. Most of the harness components a team ends up shipping were preceded by components that did not work.
- **Distribute battle-tested configurations** to the team via repository-level config. Do not reinvent per developer.
- **Optimize for iteration speed**, not for one-shotting on the first attempt. Faster cycles win.
- **Give the agent broad capabilities first**, then pare down once you know what is actually used.
- **Bias toward shipping.** Spend on harness work to the extent that it enables more high-quality code, not as a separate goal.

## Scale-tier mapping

A clearer mapping of which patterns earn their place at which scale. Use this to avoid recommending large-team patterns to solo developers.

### Solo developer

The minimum that earns its place. Most of the leverage with the least overhead.

- **AGENTS.md or CLAUDE.md** under 100 lines, often under 60. Build commands, hard constraints, anything the agent has gotten wrong before.
- **A short docs/ folder** for design notes that exceed AGENTS.md's space budget.
- **An `init.sh`** that boots the project with one command.
- **Hooks** for typecheck and lint on session stop, with silent-success and verbose-failure semantics.
- **A pre-commit hook** that blocks edits to test files.
- **A typed language or strict mode** of a typed language for free back-pressure.
- **Block destructive bash patterns** with a single hook.
- **Run the agent in a sandbox** (Docker container or VM), not on the host. No production credentials in the agent's environment.

### Small team (2 to 10 engineers)

Adds collaborative discipline. Several patterns now earn their place because the team can absorb the maintenance cost.

- **Architectural enforcement** via custom linters or structural tests for layer boundaries.
- **The docs system of record**: structured `docs/` tree with design docs, exec plans, product specs, vendored references.
- **Plans as first-class artifacts** for multi-session work.
- **JSON state files** for trackable progress across sessions.
- **Sub-agents for context control** in tasks involving substantial codebase exploration.
- **Light golden principles**: three to five opinionated rules in a `STYLE.md` or similar.
- **Manual cleanup discipline**: when you fix the same kind of thing twice, encode it. Promote rules from doc to lint when mechanically checkable.
- **Selective test runs** per PR, not the full suite.
- **The two-attempt cap** on CI loops.
- **A `QUALITY_SCORE.md`** if quality drift becomes a recurring discussion in retros.

### Larger team or organization

Adds the patterns that need engineering investment but compound at scale.

- **Scheduled cleanup agents** that scan for golden-principle violations and open targeted refactor PRs.
- **A doc-gardening agent** that scans for stale documentation.
- **Quality-grading automation** that updates `QUALITY_SCORE.md` on a cadence.
- **Multi-agent patterns** (planner/generator/evaluator) for tasks where evaluation is hard.
- **Devbox-style sandboxes**: pre-warmed, isolated, identical to human dev environments.
- **A per-worktree observability stack** for performance and correctness work.
- **A toolshed-style centralized internal MCP** if there are many internal tools.
- **Throughput-aware merge philosophy**: minimal blocking gates, agent-to-agent review, short-lived PRs, shift feedback left.
- **Conditional rules at subdirectory granularity** in monorepos.
- **Audit logging** of all agent actions.
- **Adaptive throttling and circuit breakers** for unattended workflows.
- **Harness-as-template across repos**: shared starter harnesses for common application topologies.

### Cross-cutting (any scale)

These patterns earn their place regardless of team size. Worth checking that solo developers and large teams alike have them.

- **The diagnostic loop**: when the agent fails, ask what capability is missing and how to make it legible and enforceable.
- **Earn each rule**: every constraint traces to a specific past failure or hard external constraint.
- **Strongly-worded behavioral constraints** in AGENTS.md when soft instructions have failed.
- **The map-not-manual principle** for AGENTS.md.
- **Silent success, verbose failure** for every verification hook.
- **Read what you install** for MCP servers and skills.
- **Re-examine the harness** on every major model release.

## When to flag uncertainty to the user

Be honest about open questions in the literature. The skill should not pretend to certainty it does not have.

- How architectural coherence holds in fully agent-generated codebases over years is unproven. The longest public examples are five months.
- The right division between human judgment and encoded rules is still being learned.
- Whether harnesses converge across organizations into a small set of templates ("golden paths"), or whether each team's harness stays bespoke, is open.
- Whether single-agent or multi-agent architectures perform better for general coding work is genuinely unsettled. Anthropic's data suggests multi-agent helps when the task sits at the model's edge but adds overhead when the task is well within reach.

When the user asks about something in this territory, name it as open and offer the best current thinking rather than pretending there is consensus.
