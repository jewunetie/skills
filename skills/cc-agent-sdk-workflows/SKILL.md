---
name: cc-agent-sdk-workflows
description: >
  Build Python workflows and agents using the Claude Agent SDK (claude-agent-sdk).
  Use this skill whenever the user wants to create, design, or debug agent workflows,
  multi-agent systems, automation scripts, or any Python code that uses the Claude Agent SDK
  (formerly Claude Code SDK). Trigger on mentions of: "agent sdk", "claude-agent-sdk",
  "claude_agent_sdk", "query()", "ClaudeSDKClient", "subagents", "AgentDefinition",
  "agent workflow", "multi-agent", "claude code sdk", or any request to build an
  autonomous agent that reads files, runs commands, edits code, or orchestrates tasks
  programmatically. Also trigger when the user asks about architecting agent systems,
  choosing between SDK patterns, or integrating custom tools/hooks/MCP servers with
  the Agent SDK. Even if the user just says "build me an agent" or "automate this with
  Claude", use this skill.
---

# Claude Agent SDK Workflow Builder

Build production Python agents and workflows using the Claude Agent SDK.

## Before generating any code

1. Read `references/api-reference.md` for types, signatures, and defaults.
2. Read `references/patterns.md` for the workflow template closest to the user's need.
3. Read `references/gotchas.md` to avoid common mistakes.

Only after reading the relevant references should you write or propose code.

## Full documentation links

When deeper detail is needed beyond what these references provide:

- Python SDK reference: https://platform.claude.com/docs/en/agent-sdk/python
- SDK overview: https://platform.claude.com/docs/en/agent-sdk/overview
- Subagents guide: https://platform.claude.com/docs/en/agent-sdk/subagents
- Hooks guide: https://platform.claude.com/docs/en/agent-sdk/hooks
- Custom tools: https://platform.claude.com/docs/en/agent-sdk/custom-tools
- MCP in the SDK: https://platform.claude.com/docs/en/agent-sdk/mcp
- Structured outputs: https://platform.claude.com/docs/en/agent-sdk/structured-outputs
- Permissions and user input: https://platform.claude.com/docs/en/agent-sdk/user-input
- Session management: https://platform.claude.com/docs/en/agent-sdk/sessions
- File checkpointing: https://platform.claude.com/docs/en/agent-sdk/file-checkpointing
- Hosting/deployment: https://platform.claude.com/docs/en/agent-sdk/hosting
- Plugins: https://platform.claude.com/docs/en/agent-sdk/plugins
- Agent Skills: https://platform.claude.com/docs/en/agent-sdk/skills
- Slash commands: https://platform.claude.com/docs/en/agent-sdk/slash-commands
- Tracking costs: https://platform.claude.com/docs/en/agent-sdk/cost-tracking
- GitHub repo: https://github.com/anthropics/claude-agent-sdk-python

If you are uncertain about any SDK behavior, fetch the relevant documentation page
before generating code rather than guessing.

---

## Decision Framework

Use this flowchart to choose the right SDK pattern for the user's workflow.

### Step 1: Session model

Ask: Does the workflow need multi-turn conversation or response-driven branching?

- **No** (independent task, fire-and-forget) --> Use `query()`.
- **Yes** (follow-ups, interrupts, conditional next steps) --> Use `ClaudeSDKClient`.

Also use `ClaudeSDKClient` if the workflow needs any of:
- Interrupt capability
- File checkpointing with rewind
- Multi-turn conversation memory

Note: Hooks and custom MCP tools work with both `query()` and `ClaudeSDKClient`
(they are configured via `ClaudeAgentOptions` which both interfaces accept). The SDK
reference comparison table may list these as `ClaudeSDKClient`-only, but official
examples demonstrate them working with `query()`. When in doubt, prefer
`ClaudeSDKClient` for complex workflows combining multiple features.

### Step 2: Agent decomposition

Ask: Is the task a single coherent job, or does it have distinct subtasks that benefit
from isolated context, parallelism, or specialized prompts?

- **Single job** --> One agent (via `query()` or `ClaudeSDKClient`).
- **Multiple distinct subtasks** --> Define subagents with `AgentDefinition`. Include
  `"Task"` in `allowed_tools` on the parent agent.

Subagents are valuable when:
- Subtasks should not pollute each other's context (e.g., a security scanner should not
  see the style checker's intermediate reasoning).
- Subtasks can run in parallel (Claude determines this automatically).
- Subtasks need different system prompts, tool sets, or models.

### Step 3: External integrations

Ask: Does the workflow need to call external services, APIs, or custom logic?

- **No** --> Use only built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebFetch,
  WebSearch, etc.).
- **Yes, simple callable functions** --> Define custom MCP tools with `@tool` +
  `create_sdk_mcp_server()`. These run in-process with no subprocess overhead.
- **Yes, existing MCP servers** --> Add them to `mcp_servers` as stdio, SSE, or HTTP
  configs. Can be mixed with SDK MCP servers.

### Step 4: Governance and safety

Ask: Does the workflow need guardrails, logging, or behavior modification?

- **Block dangerous commands** --> PreToolUse hook that returns a deny decision.
- **Audit/log tool usage** --> PostToolUse hook that logs to file or external service.
- **Modify prompts on the fly** --> UserPromptSubmit hook.
- **Monitor subagent completion** --> SubagentStop hook.
- **Custom permission logic** --> `can_use_tool` callback on `ClaudeAgentOptions`.
- **No governance needed** --> Skip hooks; use `permission_mode="acceptEdits"` or
  `"bypassPermissions"` as appropriate.

### Step 5: Output format

Ask: Does the workflow need structured, machine-readable output?

- **Yes** --> Use `output_format={"type": "json_schema", "schema": {...}}` in options.
- **No** --> Let Claude respond naturally.

### Step 6: Sandboxing

Ask: Should commands run in a restricted sandbox?

- **Yes** --> Configure `sandbox={"enabled": True, ...}` in options.
- **No** --> Omit sandbox settings (default).

---

## Architecture Guidance

### Decomposing workflows into agents

Think of agents like functions: each should have a single, clear responsibility.
A good decomposition follows these heuristics:

- If a subtask produces intermediate artifacts that the main agent does not need to see,
  make it a subagent.
- If a subtask has a distinct expertise or system prompt, make it a subagent.
- If subtasks are independent and could run simultaneously, make them separate subagents
  (Claude will parallelize automatically).
- If all tasks are sequential and share context, keep them in one agent.

### Permission strategy

Choose the most restrictive mode that still lets the workflow function:

- `"default"` -- Prompts for each tool use. Good for interactive sessions.
- `"acceptEdits"` -- Auto-accepts file reads/writes. Good for automation scripts.
- `"bypassPermissions"` -- No permission checks. Use only in trusted, sandboxed
  environments.
- Custom `can_use_tool` callback -- Fine-grained control per tool invocation.

### Session and state management

- `query()` creates a fresh session every call. No state carries over.
- `ClaudeSDKClient` maintains session state across multiple `.query()` calls.
- To resume a previous session: use `resume=session_id` in options.
- To fork a session (branch from a point): use `resume=session_id` + `fork_session=True`.
- To load project context (CLAUDE.md files): set `setting_sources=["project"]`.

### Error handling

Every workflow should:

1. Catch `CLINotFoundError` -- the Claude Code CLI is bundled but may not be available.
2. Catch `ProcessError` -- includes `exit_code` and `stderr` for debugging.
3. Catch `CLIJSONDecodeError` -- malformed output from the CLI.
4. Extract cost/usage from `ResultMessage` for monitoring.

### Cost tracking

`ResultMessage` includes `total_cost_usd`, `usage`, `duration_ms`, and `num_turns`.
Always capture these for production workflows. For subagents, the Task tool output
includes its own `total_cost_usd` and `duration_ms`.

---

## Code Generation Standards

When generating SDK workflow code, always:

1. Use `asyncio.run(main())` as the entry point (or `anyio.run(main)` if the user
   prefers anyio).
2. Include proper error handling with the SDK's exception hierarchy.
3. Use type-aware message processing (isinstance checks for AssistantMessage,
   ResultMessage, etc.).
4. Extract and print/log `ResultMessage` fields (cost, duration, session_id).
5. Add docstrings explaining what the workflow does and what each agent's role is.
6. Use meaningful `description` fields in `AgentDefinition` so Claude knows when to
   invoke each subagent.
7. Set `permission_mode` explicitly rather than relying on the default.
8. Never assume `setting_sources` loads anything by default -- it does not.
9. If the workflow uses subagents, include `"Task"` in `allowed_tools`.
10. Prefer `async with ClaudeSDKClient() as client:` context manager for lifecycle.

---

## Workflow Complexity Tiers

Use this to calibrate response depth:

**Tier 1 -- Simple script** (query-based, single agent, built-in tools only):
Generate a single Python file. Minimal boilerplate.

**Tier 2 -- Interactive agent** (ClaudeSDKClient, multi-turn, maybe hooks):
Generate a single Python file with a class or structured functions.

**Tier 3 -- Multi-agent system** (subagents, custom tools, hooks, MCP):
Propose a file structure first. Separate concerns: agent definitions, tool definitions,
hook definitions, main orchestrator. Confirm structure with user before generating.
