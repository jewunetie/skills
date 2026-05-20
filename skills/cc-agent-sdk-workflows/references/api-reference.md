# API Reference (Condensed)

Quick reference for the Claude Agent SDK Python types, signatures, and defaults.
This covers the parts that are easy to get wrong or forget. For complete details:
https://platform.claude.com/docs/en/agent-sdk/python

---

## Table of Contents

1. [Installation and Prerequisites](#installation-and-prerequisites)
2. [Core Functions](#core-functions)
3. [ClaudeSDKClient](#claudesdkclient)
4. [ClaudeAgentOptions](#claudeagentoptions)
5. [AgentDefinition (Subagents)](#agentdefinition-subagents)
6. [Custom Tools and MCP Servers](#custom-tools-and-mcp-servers)
7. [Hooks](#hooks)
8. [Message Types](#message-types)
9. [Content Block Types](#content-block-types)
10. [Error Types](#error-types)
11. [Permission Types](#permission-types)
12. [Output Format](#output-format)
13. [Sandbox Settings](#sandbox-settings)
14. [Built-in Tool Names](#built-in-tool-names)

---

## Installation and Prerequisites

```bash
pip install claude-agent-sdk
```

- Requires Python 3.10+.
- The Claude Code CLI is bundled automatically -- no separate install needed.
- To use a custom CLI path: `ClaudeAgentOptions(cli_path="/path/to/claude")`.

---

## Core Functions

### query()

Creates a new session per call. No conversation memory between calls.

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None
) -> AsyncIterator[Message]
```

- `prompt` can be a string or an async iterable of dicts for streaming input.
- Returns `AsyncIterator[Message]` -- iterate with `async for`.
- Each call starts a fresh session.

### tool()

Decorator for defining custom MCP tools.

```python
@tool(name: str, description: str, input_schema: type | dict)
async def my_tool(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": "result"}]}
```

Input schema options:
- Simple: `{"name": str, "count": int}` (recommended)
- JSON Schema: `{"type": "object", "properties": {...}, "required": [...]}`

Return format must always be: `{"content": [{"type": "text", "text": "..."}]}`
For errors, add `"is_error": True` to the return dict.

### create_sdk_mcp_server()

```python
def create_sdk_mcp_server(
    name: str,
    version: str = "1.0.0",
    tools: list[SdkMcpTool[Any]] | None = None
) -> McpSdkServerConfig
```

Returns config to pass into `ClaudeAgentOptions.mcp_servers`.

---

## ClaudeSDKClient

Maintains a conversation session across multiple exchanges. Supports custom tools,
hooks, interrupts, and file checkpointing.

```python
class ClaudeSDKClient:
    def __init__(self, options: ClaudeAgentOptions | None = None)
    async def connect(self, prompt=None) -> None
    async def query(self, prompt, session_id="default") -> None
    async def receive_messages(self) -> AsyncIterator[Message]   # All messages
    async def receive_response(self) -> AsyncIterator[Message]   # Until ResultMessage
    async def interrupt(self) -> None
    async def rewind_files(self, user_message_uuid: str) -> None  # Requires enable_file_checkpointing=True
    async def disconnect(self) -> None
```

Context manager usage (preferred):
```python
async with ClaudeSDKClient(options) as client:
    await client.query("Do something")
    async for msg in client.receive_response():
        process(msg)
```

Key difference between `receive_messages()` and `receive_response()`:
- `receive_response()` stops after a `ResultMessage` (one turn).
- `receive_messages()` yields all messages indefinitely.

---

## ClaudeAgentOptions

All fields are optional. Defaults shown.

```python
@dataclass
class ClaudeAgentOptions:
    allowed_tools: list[str] = []
    system_prompt: str | SystemPromptPreset | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = {}
    permission_mode: PermissionMode | None = None        # "default"|"acceptEdits"|"plan"|"bypassPermissions"
    continue_conversation: bool = False
    resume: str | None = None                             # Session ID to resume
    max_turns: int | None = None
    disallowed_tools: list[str] = []
    model: str | None = None
    output_format: OutputFormat | None = None
    cwd: str | Path | None = None
    setting_sources: list[SettingSource] | None = None    # IMPORTANT: defaults to None (no settings loaded)
    add_dirs: list[str | Path] = []
    env: dict[str, str] = {}
    can_use_tool: CanUseTool | None = None
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    agents: dict[str, AgentDefinition] | None = None
    include_partial_messages: bool = False
    fork_session: bool = False
    enable_file_checkpointing: bool = False
    sandbox: SandboxSettings | None = None
    plugins: list[SdkPluginConfig] = []
    extra_args: dict[str, str | None] = {}
    stderr: Callable[[str], None] | None = None
    user: str | None = None
    cli_path: str | None = None                           # Override bundled CLI path
```

### SystemPromptPreset

To use Claude Code's built-in system prompt (with optional additions):

```python
system_prompt = {
    "type": "preset",
    "preset": "claude_code",
    "append": "Additional instructions here"  # optional
}
```

### SettingSource

Controls which filesystem settings are loaded.

```python
SettingSource = Literal["user", "project", "local"]
```

- `"user"` -- `~/.claude/settings.json`
- `"project"` -- `.claude/settings.json` (also loads CLAUDE.md files)
- `"local"` -- `.claude/settings.local.json`
- Default is `None` -- **no settings loaded at all**.

---

## AgentDefinition (Subagents)

```python
@dataclass
class AgentDefinition:
    description: str                                              # When to use (Claude reads this)
    prompt: str                                                   # System prompt for the subagent
    tools: list[str] | None = None                                # Inherits parent tools if None
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None  # Inherits parent model if None
```

Usage in options:
```python
ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Task"],   # "Task" is REQUIRED for subagents
    agents={
        "reviewer": AgentDefinition(
            description="Code quality and security reviewer.",
            prompt="Review code for bugs, security issues, and style.",
            tools=["Read", "Glob", "Grep"],
            model="sonnet"
        )
    }
)
```

Subagents are invoked via the `Task` tool. Claude decides when to invoke them
based on the `description` field.

---

## Custom Tools and MCP Servers

### In-process SDK MCP tools (recommended for custom logic)

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("tool_name", "Description of what it does", {"param": str})
async def my_tool(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Result: {args['param']}"}]}

server = create_sdk_mcp_server(name="my_server", tools=[my_tool])

options = ClaudeAgentOptions(
    mcp_servers={"my_server": server},
    allowed_tools=["mcp__my_server__tool_name"]   # naming convention: mcp__<server>__<tool>
)
```

### External MCP servers

```python
# Stdio (subprocess)
{"type": "stdio", "command": "python", "args": ["-m", "my_server"], "env": {"KEY": "val"}}

# SSE
{"type": "sse", "url": "https://example.com/sse", "headers": {"Authorization": "Bearer ..."}}

# HTTP
{"type": "http", "url": "https://example.com/mcp", "headers": {}}
```

### Mixing server types

```python
mcp_servers={
    "internal": sdk_server,                                      # In-process
    "external": {"type": "stdio", "command": "external-server"}  # Subprocess
}
```

---

## Hooks

Hooks intercept specific events in the agent loop. They are Python async callbacks.

### Supported events (Python SDK)

| Event             | When it fires                    | Can block? |
|-------------------|----------------------------------|------------|
| PreToolUse        | Before a tool executes           | Yes (deny) |
| PostToolUse       | After a tool executes            | No         |
| UserPromptSubmit  | When user submits a prompt       | No (but can modify prompt) |
| Stop              | When the agent stops             | No         |
| SubagentStop      | When a subagent finishes         | No         |
| PreCompact        | Before message compaction        | No         |

**Not available in Python SDK:** SessionStart, SessionEnd, Notification.

### Hook signature

```python
async def my_hook(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    # Return {} to take no action
    # Return {"hookSpecificOutput": {...}} to modify behavior
    return {}
```

### HookMatcher

```python
@dataclass
class HookMatcher:
    matcher: str | None = None          # Tool name or pattern, e.g. "Bash", "Write|Edit"
    hooks: list[HookCallback] = []
    timeout: float | None = None        # Seconds (default: 60)
```

- `matcher=None` means the hook fires for all tools.
- `matcher` only matches tool names, not file paths or arguments.

### PreToolUse deny pattern

```python
async def block_dangerous(input_data, tool_use_id, context):
    if "rm -rf" in input_data.get("tool_input", {}).get("command", ""):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Dangerous command blocked"
            }
        }
    return {}
```

### UserPromptSubmit modify pattern

```python
async def add_context(input_data, tool_use_id, context):
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "updatedPrompt": f"[context] {input_data.get('prompt', '')}"
        }
    }
```

---

## Message Types

```python
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage
```

| Type             | Key fields                                                        |
|------------------|-------------------------------------------------------------------|
| UserMessage      | `content: str \| list[ContentBlock]`                              |
| AssistantMessage | `content: list[ContentBlock]`, `model: str`                       |
| SystemMessage    | `subtype: str`, `data: dict`                                      |
| ResultMessage    | `is_error`, `result`, `session_id`, `total_cost_usd`, `usage`, `duration_ms`, `num_turns` |

### Processing pattern

```python
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock, ToolUseBlock

async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
            elif isinstance(block, ToolUseBlock):
                print(f"Tool: {block.name}, Input: {block.input}")
    elif isinstance(message, ResultMessage):
        if message.total_cost_usd is not None:
            print(f"Cost: ${message.total_cost_usd}, Turns: {message.num_turns}")
        if message.is_error:
            print(f"Error: {message.result}")
```

---

## Content Block Types

```python
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

| Type            | Key fields                                      |
|-----------------|-------------------------------------------------|
| TextBlock       | `text: str`                                     |
| ThinkingBlock   | `thinking: str`, `signature: str`               |
| ToolUseBlock    | `id: str`, `name: str`, `input: dict`           |
| ToolResultBlock | `tool_use_id: str`, `content`, `is_error: bool` |

---

## Error Types

```python
ClaudeSDKError           # Base exception
  CLIConnectionError     # Connection to CLI failed
    CLINotFoundError     # CLI not installed / not found
  ProcessError           # Process failed (has exit_code, stderr)
  CLIJSONDecodeError     # JSON parsing failed (has line, original_error)
```

---

## Permission Types

### PermissionMode

```python
PermissionMode = Literal["default", "acceptEdits", "plan", "bypassPermissions"]
```

### Custom permission callback (can_use_tool)

```python
async def my_permission_handler(
    tool_name: str,
    input_data: dict,
    context: dict
) -> PermissionResultAllow | PermissionResultDeny:
    if should_allow(tool_name, input_data):
        return PermissionResultAllow(updated_input=input_data)
    else:
        return PermissionResultDeny(message="Not allowed", interrupt=True)
```

`PermissionResultAllow` can modify the tool input via `updated_input`.
`PermissionResultDeny` can set `interrupt=True` to stop execution entirely.

---

## Output Format

For structured, machine-readable output:

```python
output_format = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "issues": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["summary", "issues"]
    }
}
```

Pass as `ClaudeAgentOptions(output_format=output_format)`.

---

## Sandbox Settings

```python
# SandboxSettings is a TypedDict -- pass as a plain dict
sandbox = {
    "enabled": True,
    "autoAllowBashIfSandboxed": True,
    "excludedCommands": ["docker"],             # Always bypass sandbox
    "allowUnsandboxedCommands": False,          # Model cannot request unsandboxed
    "network": {
        "allowLocalBinding": True,              # For dev servers
        "allowUnixSockets": [],
    },
}
```

Filesystem and network access restrictions are controlled by permission rules,
not sandbox settings.

---

## Built-in Tool Names

For the `allowed_tools` and `disallowed_tools` fields:

| Tool Name        | Purpose                                   |
|------------------|-------------------------------------------|
| Read             | Read files                                |
| Write            | Create/overwrite files                    |
| Edit             | Edit existing files (find and replace)    |
| Bash             | Execute shell commands                    |
| Glob             | Find files by pattern                     |
| Grep             | Search file contents                      |
| WebFetch         | Fetch web page content                    |
| WebSearch        | Search the web                            |
| NotebookEdit     | Edit Jupyter notebooks                    |
| Task             | Invoke subagents (REQUIRED for subagents) |
| TodoWrite        | Manage task lists                         |
| AskUserQuestion  | Ask user clarifying questions             |
| BashOutput       | Read background shell output              |
| KillBash         | Kill background shell                     |
| ListMcpResources | List MCP server resources                 |
| ReadMcpResource  | Read a specific MCP resource              |
| ExitPlanMode     | Exit planning mode with a plan            |
| Skill            | Enable agent Skills (filesystem-based)    |

Custom MCP tool naming: `mcp__<server_name>__<tool_name>`
Example: `mcp__calculator__add`
