# 06 Tools, skills, and sub-agents

The model's tool surface is part of the harness. Every tool's name, description, and schema gets stamped into the system prompt every request. Add tools carelessly and the context window fills with descriptions before the agent has done anything. Tool selection is a context-engineering problem.

## Few good tools beat many overlapping tools

The HumanLayer rule, which matches Anthropic's own findings: 10 focused tools outperform 50 overlapping ones because the model can hold the menu in its head.

Failure mode worth recognizing: the user installs a popular MCP server, gets 30 new tools, and the agent's performance degrades because the context is now bloated with tool descriptions for things the agent does not need.

Anthropic released experimental MCP tool search precisely to mitigate this. If the user has many tools connected, the harness progressively discloses tools to the agent only when relevant. If your harness does not support tool search, the rule is: turn off MCP servers you are not actively using.

## Prefer CLIs the model already knows over MCP servers

If the agent is working with a tool that has a CLI well represented in training data (`gh`, `git`, `docker`, `kubectl`, `jq`, `curl`, common database CLIs), prompt the agent to use the CLI. Do not install an MCP server that wraps the same thing.

Reasons:

- The model has seen these tools enough during training to know the flag patterns and common idioms.
- CLIs compose with other shell tools (`grep`, `sed`, `awk`, `jq`) for context-efficient extraction.
- CLI invocations are smaller in context than MCP tool definitions.
- No additional dependency to install, no additional auth flow to manage.

HumanLayer replaced the Linear MCP server with a small custom CLI plus six example invocations in their CLAUDE.md. They saved thousands of tokens from MCP tool definitions and many more from verbose MCP responses.

The pattern: when a CLI exists, write 5 to 10 example invocations in AGENTS.md. The agent figures out the rest.

## When to use an MCP server

MCP servers earn their place when:

- They expose something with no good CLI equivalent (a custom internal API, a SaaS that requires OAuth dance every time).
- The tool's description carries useful prompt content ("when to use this tool" instructions in the description).
- The server provides resources or prompts (rare; check whether the harness supports them; many do not).
- The agent runs in an environment where installing a new CLI is impractical.

When evaluating an MCP server, ask: does this give me something I cannot get with a few lines of bash plus a CLI the agent already knows?

## Toolshed pattern (large team)

For organizations with many internal tools, Stripe's "Toolshed" pattern is worth knowing:

- A single centralized internal MCP server shared across all agent systems in the organization.
- About 500 tools consolidated into one server.
- The server does not pass through all 500 tools to every agent. It issues a carefully selected per-task subset.
- Adding a tool to Toolshed makes it immediately available to all agents.

This trades startup cost (build the server, manage tool registration, design the per-task selection logic) for compounding benefit (every team's tools are discoverable, no duplication, central security review).

## Skills: progressive disclosure of knowledge and tools

Skills (originally Anthropic, now a cross-tool open standard supported by Claude Code, Codex, OpenCode, and others) solve the "instruction budget" problem: every instruction in the system prompt competes for the agent's attention. Skills let knowledge and tools load only when the task calls for them.

A skill is a directory with a `SKILL.md` plus optional bundled files:

```text
example-skill/
  SKILL.md
  response_template.md
  CLIs/
    linear-cli
    tunnel-cli
  references/
    advanced-patterns.md
```

When the skill activates, only `SKILL.md` is injected into context. The skill itself can tell the agent what other files exist in its directory and when to read them. This is progressive disclosure two layers deep: skills hide knowledge from the system prompt; reference files within a skill hide knowledge from the SKILL.md.

The triggering description in `SKILL.md` frontmatter is the load-bearing piece. It controls whether the skill activates. Skill descriptions should be a bit "pushy" because models tend to under-trigger skills.

When to write a skill rather than putting content in AGENTS.md:

- The knowledge is task-specific (only relevant when working on a particular feature or workflow).
- It is more than 50 lines of guidance, scripts, and examples.
- It bundles small CLIs, templates, or reference docs.
- It belongs to a specific domain inside a larger codebase.

When to put content in AGENTS.md instead of a skill:

- The rule applies to every session in the project (build commands, hard constraints).
- It is a one-line instruction, not a workflow.

## A security note on skills and MCP servers

Both skills and MCP servers are dependencies. Treat them with the same scrutiny as `npm install random-package`:

- Skill registries (ClawHub, skills.sh) have been observed distributing malicious skills. A skill can execute arbitrary code on the machine.
- MCP server tool descriptions are trusted text that gets injected into the system prompt every request. A malicious or sloppy MCP server can prompt-inject the agent before the user has typed anything.
- STDIO and `uvx`/`npx`-launched MCP servers run code on the host even without prompt injection.

Practical defaults:

- Read what you are installing before installing it.
- Pin versions. Audit updates.
- Prefer first-party (Anthropic, the tool's official maintainer) over third-party packages.
- For internal tools, vendor the source rather than installing from a registry.

## Sub-agents are for context control, not role specialization

The misunderstanding worth flagging up front: sub-agents are not for role decomposition. The "frontend engineer" sub-agent and "backend engineer" sub-agent and "data analyst" sub-agent pattern does not work in practice. The HumanLayer team tried it and recommended against it.

What sub-agents are actually for: a context firewall. The parent (orchestrator) agent dispatches a task to a sub-agent. The sub-agent runs in a fresh context window, does its work (which may involve many tool calls and intermediate reasoning), and returns only its final result. None of the intermediate noise lands in the parent's context.

This is structural. Without sub-agents, the parent's context fills up with tool outputs, search results, and reasoning that does not directly inform the next decision. With sub-agents, the parent stays in the "smart zone" with a small, high-relevance context, and each sub-agent gets a fresh "instruction budget" for its task.

The Chroma context rot research backs this up empirically: model performance degrades as context length grows, even on simple tasks, and degrades faster when there is low semantic similarity between the question and the relevant content in context.

## What sub-agents do well

Tasks that fit the sub-agent pattern share a shape: a question with a short answer that takes many tool calls to find:

- Locating specific definitions or implementations in a large codebase.
- Identifying patterns across files for a specific type of work.
- Tracing the flow of a request across service boundaries.
- General code, documentation, or web research.
- Codebase exploration ("find all places that use this API and summarize how").

The sub-agent's return contract should be condensed: an answer plus citations in `filepath:line` form or with URLs, so the parent can dig in if needed without inheriting all the source material.

## Sub-agents for cost control

A second use: cost control. Use an expensive model (Opus 4.6) for the orchestrating parent where thinking-heavy work happens. Use a cheaper, faster model (Sonnet, Haiku) for sub-agents handling smaller tasks. Sub-agents typically receive narrower tasks with smaller instruction budgets, so a less expensive model is sufficient.

## Built-in versus custom sub-agents

Different harnesses handle this differently:

- Claude Code provides built-in sub-agents like `Explore` (codebase exploration) and `Bash` (verbose bash command execution). Use these before writing custom ones.
- Codex's sub-agent support is more recent and still experimental.
- For harnesses without native sub-agent support, you can implement the pattern via an MCP server that launches a new agent session with the parent's prompt and returns the final response.

A warning on the MCP-based pattern: if the parent harness supports sub-agents and you also expose this MCP-based sub-agent dispatcher, sub-agents can spawn sub-agents and the chain becomes hard to debug ("game of telephone"). Watch tool call timeouts; raise them if needed.

## Specifying sub-agent prompts

When writing the system prompt for a sub-agent, be specific about three things:

1. **Role and scope.** What is the sub-agent allowed to do, and what is it not allowed to do.
2. **Return contract.** What information should the sub-agent return, and in what format. Citations, line numbers, condensed summaries.
3. **Available tools.** Which tools the sub-agent should have, and which it should not. Less is usually more.

Vague sub-agent prompts produce sub-agents that wander, return verbose responses, or do too much.

## Solo developer minimum

A solo developer working in Claude Code or Cursor can usually skip MCP servers entirely. Tools that come with the harness (file edit, bash, web search) plus a few CLIs invoked via bash cover most cases.

Sub-agents are still useful for solo developers, especially the built-in codebase exploration sub-agents. Use them when a task would otherwise involve grepping through many files or reading lots of source material.

Skills are worth writing once you find yourself repeating the same workflow with the agent in a particular project. Until then, AGENTS.md is enough.
