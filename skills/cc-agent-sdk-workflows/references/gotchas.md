# Gotchas and Common Mistakes

Things that are easy to get wrong with the Claude Agent SDK. Read this before
generating code to avoid debugging sessions.

For full documentation: https://platform.claude.com/docs/en/agent-sdk/python

---

## Table of Contents

1. [Subagents require "Task" in allowed_tools](#1-subagents-require-task-in-allowed_tools)
2. [setting_sources defaults to None](#2-setting_sources-defaults-to-none)
3. [Python SDK hook limitations](#3-python-sdk-hook-limitations)
4. [Do not break out of async message iteration](#4-do-not-break-out-of-async-message-iteration)
5. [Subagents do not inherit permissions](#5-subagents-do-not-inherit-permissions)
6. [MCP tool naming convention](#6-mcp-tool-naming-convention)
7. [Tool return format must follow the MCP spec](#7-tool-return-format-must-follow-the-mcp-spec)
8. [Bundled CLI vs system CLI](#8-bundled-cli-vs-system-cli)
9. [anyio vs asyncio](#9-anyio-vs-asyncio)
10. [Hook matchers only match tool names](#10-hook-matchers-only-match-tool-names)
11. [UserPromptSubmit hooks and subagent loops](#11-userpromptsubmit-hooks-and-subagent-loops)
12. [ResultMessage.result may be None](#12-resultmessageresult-may-be-none)
13. [Sandbox does not control filesystem or network access](#13-sandbox-does-not-control-filesystem-or-network-access)
14. [Permission callback signature](#14-permission-callback-signature)
15. [cost and usage fields can be None](#15-cost-and-usage-fields-can-be-none)
16. [Hooks and custom tools: query() vs ClaudeSDKClient docs inconsistency](#16-hooks-and-custom-tools-query-vs-claudesdkclient-docs-inconsistency)

---

## 1. Subagents require "Task" in allowed_tools

If you define agents in `ClaudeAgentOptions.agents` but forget to add `"Task"` to
`allowed_tools`, Claude will never invoke the subagents. There will be no error --
they simply will not be used.

```python
# WRONG -- subagents defined but Task not in allowed_tools
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write"],
    agents={"reviewer": AgentDefinition(...)},
)

# CORRECT
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Task"],
    agents={"reviewer": AgentDefinition(...)},
)
```

---

## 2. setting_sources defaults to None

By default, the SDK loads **no** filesystem settings. This means:
- CLAUDE.md files in the project are **not** loaded.
- `~/.claude/settings.json` is **not** loaded.
- `.claude/settings.json` is **not** loaded.

If you want project context or filesystem-based agents/skills, you must opt in:

```python
# Load project settings (including CLAUDE.md)
ClaudeAgentOptions(setting_sources=["project"])

# Load all settings
ClaudeAgentOptions(setting_sources=["user", "project", "local"])
```

This is intentional: it provides isolation for SDK applications.

---

## 3. Python SDK hook limitations

The Python SDK does **not** support these hook events:
- `SessionStart`
- `SessionEnd`
- `Notification`

These are only available in the TypeScript SDK. If you need them, use the
TypeScript SDK or implement equivalent logic in your Python application code.

---

## 4. Do not break out of async message iteration

Using `break` to exit `async for message in client.receive_response()` early
can cause asyncio cleanup issues.

```python
# WRONG -- may cause asyncio errors
async for message in client.receive_response():
    if isinstance(message, ResultMessage):
        break  # Do not do this

# CORRECT -- use a flag and let the loop finish
found_result = False
async for message in client.receive_response():
    if isinstance(message, ResultMessage):
        found_result = True
        result = message
    # Let the iteration complete naturally
```

---

## 5. Subagents do not inherit permissions

Each subagent starts with a clean permission state. If the parent agent's PreToolUse
hook auto-approves certain tools, subagents will **not** automatically benefit from
that approval.

To avoid repeated permission prompts across subagents:
- Use PreToolUse hooks that apply to all sessions.
- Or configure permission rules in the settings that apply globally.
- Or use `permission_mode="acceptEdits"` / `"bypassPermissions"` which applies to
  the entire session including subagents.

---

## 6. MCP tool naming convention

Custom MCP tools must be referenced with the pattern `mcp__<server_name>__<tool_name>`.
Note: that is **two underscores** on each side of the server name.

```python
# If server name is "my_server" and tool name is "my_tool":
allowed_tools=["mcp__my_server__my_tool"]

# Common mistake: single underscores
allowed_tools=["mcp_my_server_my_tool"]  # WRONG
```

---

## 7. Tool return format must follow the MCP spec

Custom tools defined with `@tool` must return a dict with a `content` key containing
a list of content blocks.

```python
# CORRECT
return {"content": [{"type": "text", "text": "result"}]}

# WRONG -- returning a plain string
return "result"

# WRONG -- missing content wrapper
return {"text": "result"}

# For errors, add is_error
return {"content": [{"type": "text", "text": "Error occurred"}], "is_error": True}
```

---

## 8. Bundled CLI vs system CLI

The `claude-agent-sdk` pip package bundles the Claude Code CLI automatically.
You do **not** need to install it separately. However:

- If you have a system-wide Claude Code installation, the SDK uses the bundled
  version by default.
- To use a specific CLI: `ClaudeAgentOptions(cli_path="/path/to/claude")`.
- If you get `CLINotFoundError`, try reinstalling the package:
  `pip install --force-reinstall claude-agent-sdk`.

---

## 9. anyio vs asyncio

The SDK works with both `asyncio` and `anyio`. The README examples use `anyio.run(main)`,
but `asyncio.run(main())` works identically. Choose based on your project's async
framework.

```python
# Both work
import asyncio
asyncio.run(main())

# Or
import anyio
anyio.run(main)  # Note: no parentheses on main
```

---

## 10. Hook matchers only match tool names

`HookMatcher.matcher` matches against the **tool name** only (e.g., "Bash",
"Write", "Edit"). It does **not** match against:
- File paths
- Command strings
- Tool arguments

To filter by file path or command content, check inside the hook callback itself:

```python
# Matcher only filters by tool name
HookMatcher(matcher="Write", hooks=[my_hook])

# Inside the hook, check specific arguments
async def my_hook(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "")
    if file_path.startswith("/protected/"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Access to /protected/ is not allowed",
            }
        }
    return {}
```

---

## 11. UserPromptSubmit hooks and subagent loops

A `UserPromptSubmit` hook that spawns subagents can create infinite loops if those
subagents trigger the same hook. Protect against this:

```python
async def my_prompt_hook(input_data, tool_use_id, context):
    # Check if we are already inside a subagent
    if input_data.get("parent_tool_use_id"):
        return {}  # Skip -- we are in a subagent
    # ... your logic here
    return {}
```

---

## 12. ResultMessage.result may be None

`ResultMessage.result` is `str | None`. It contains the final text output, but may
be `None` if the agent completed without a text result (e.g., it only performed
tool operations).

```python
# Always check before using
if isinstance(message, ResultMessage):
    if message.result:
        print(message.result)
    else:
        print("Agent completed without text output")
```

Similarly, `total_cost_usd` and `usage` can be `None`.

---

## 13. Sandbox does not control filesystem or network access

The `sandbox` option in `ClaudeAgentOptions` controls **command execution** sandboxing
only. Filesystem read/write restrictions and network restrictions are controlled by
**permission rules**, not sandbox settings.

```python
# This sandboxes bash commands, NOT file access
sandbox={"enabled": True, "autoAllowBashIfSandboxed": True}

# File access is controlled by permission_mode and can_use_tool callback
```

---

## 14. Permission callback signature

The `can_use_tool` callback receives three arguments, not two. The third is a context
object.

```python
# CORRECT
async def handler(tool_name: str, input_data: dict, context: dict):
    return PermissionResultAllow(updated_input=input_data)

# WRONG -- missing context parameter
async def handler(tool_name: str, input_data: dict):
    return PermissionResultAllow(updated_input=input_data)
```

---

## 15. cost and usage fields can be None

`ResultMessage.total_cost_usd` and `ResultMessage.usage` are both optional and
may be `None`. Always handle this:

```python
if isinstance(message, ResultMessage):
    cost = message.total_cost_usd
    if cost is not None:
        print(f"Cost: ${cost:.4f}")
    else:
        print("Cost information not available")
```

This can happen in certain configurations or when the CLI does not report usage
information.

---

## 16. Hooks and custom tools: query() vs ClaudeSDKClient docs inconsistency

The SDK reference comparison table says hooks and custom tools are "Not supported"
with `query()`. However, the official SDK overview page demonstrates hooks working
with `query()`, and `ClaudeAgentOptions` (which `query()` accepts) has both `hooks`
and `mcp_servers` fields.

In practice, both features appear to work with `query()` since they are configured
via the shared options object. When the official docs disagree with themselves,
prefer the approach shown in the overview page examples. For maximum safety,
use `ClaudeSDKClient` for complex workflows that combine hooks, custom tools,
and multi-turn logic.
