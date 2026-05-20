# Workflow Patterns and Templates

Working, copy-paste-ready skeletons for common Agent SDK patterns.
Each template is a minimal but complete example that can be extended.

For full API details, see `references/api-reference.md` or the official docs:
https://platform.claude.com/docs/en/agent-sdk/python

---

## Table of Contents

1. [Single-Agent Automation (query)](#1-single-agent-automation-query)
2. [Multi-Turn Interactive (ClaudeSDKClient)](#2-multi-turn-interactive-claudesdkclient)
3. [Multi-Agent Orchestration (Subagents)](#3-multi-agent-orchestration-subagents)
4. [Custom MCP Tools](#4-custom-mcp-tools)
5. [Hooks for Governance](#5-hooks-for-governance)
6. [Structured Output](#6-structured-output)
7. [Combined: Multi-Agent + Hooks + Custom Tools](#7-combined-multi-agent--hooks--custom-tools)
8. [Session Resumption and Forking](#8-session-resumption-and-forking)
9. [Streaming Input](#9-streaming-input)
10. [Sandboxed Execution](#10-sandboxed-execution)

---

## 1. Single-Agent Automation (query)

Use for one-off, fire-and-forget tasks with no conversation memory needed.

```python
import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    CLINotFoundError,
    ProcessError,
)


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
        system_prompt="You are a senior Python developer. Follow PEP 8.",
        max_turns=10,
    )

    try:
        async for message in query(
            prompt="Refactor utils.py to split it into separate modules by responsibility.",
            options=options,
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        print(f"[tool] {block.name}: {block.input}")
            elif isinstance(message, ResultMessage):
                print(f"\n--- Done ---")
                print(f"Session: {message.session_id}")
                print(f"Cost: ${message.total_cost_usd or 'N/A'}")
                print(f"Turns: {message.num_turns}")
                print(f"Duration: {message.duration_ms}ms")
                if message.is_error:
                    print(f"Error: {message.result}")
    except CLINotFoundError:
        print("Claude Code CLI not found. Run: pip install claude-agent-sdk")
    except ProcessError as e:
        print(f"Process failed (exit {e.exit_code}): {e.stderr}")


asyncio.run(main())
```

---

## 2. Multi-Turn Interactive (ClaudeSDKClient)

Use when you need conversation continuity, response-driven logic, or interrupts.

```python
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Bash"],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
    )

    async with ClaudeSDKClient(options) as client:
        # First turn
        await client.query("List all Python files in src/ and summarize what each does.")
        result_text = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        result_text += block.text
            elif isinstance(message, ResultMessage):
                session_id = message.session_id

        print(result_text)

        # Second turn -- Claude remembers the first turn
        await client.query("Now add type hints to the file with the most functions.")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Cost: ${message.total_cost_usd or 'N/A'}")


asyncio.run(main())
```

---

## 3. Multi-Agent Orchestration (Subagents)

Use when the task has distinct subtasks that benefit from isolated context,
parallelism, or specialized prompts.

```python
import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)


async def main():
    options = ClaudeAgentOptions(
        # "Task" is REQUIRED for the parent to invoke subagents
        allowed_tools=["Read", "Edit", "Bash", "Glob", "Grep", "Task"],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
        agents={
            "security-scanner": AgentDefinition(
                description="Scans code for security vulnerabilities, injection risks, and unsafe patterns.",
                prompt=(
                    "You are a security expert. Scan the provided code for:\n"
                    "- SQL injection\n"
                    "- XSS vulnerabilities\n"
                    "- Insecure deserialization\n"
                    "- Hardcoded secrets\n"
                    "Report each finding with file, line, severity, and remediation."
                ),
                tools=["Read", "Glob", "Grep"],
                model="sonnet",
            ),
            "style-checker": AgentDefinition(
                description="Reviews code style, naming conventions, and documentation quality.",
                prompt=(
                    "You are a code style reviewer. Check for:\n"
                    "- PEP 8 compliance\n"
                    "- Meaningful variable names\n"
                    "- Missing docstrings\n"
                    "- Dead code\n"
                    "Provide specific suggestions for each issue found."
                ),
                tools=["Read", "Glob", "Grep"],
                model="haiku",
            ),
            "test-writer": AgentDefinition(
                description="Writes unit tests for code that lacks test coverage.",
                prompt=(
                    "You are a test engineer. For each source file:\n"
                    "1. Identify functions without tests.\n"
                    "2. Write pytest tests covering happy path and edge cases.\n"
                    "3. Place tests in tests/ mirroring the source structure."
                ),
                tools=["Read", "Write", "Glob", "Grep", "Bash"],
                model="sonnet",
            ),
        },
    )

    async for message in query(
        prompt=(
            "Review this Python project. Use the security-scanner to find vulnerabilities, "
            "the style-checker to review code quality, and the test-writer to add missing tests. "
            "Then summarize all findings."
        ),
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    if block.name == "Task":
                        print(f"\n[subagent] {block.input.get('description', '')}")
        elif isinstance(message, ResultMessage):
            print(f"\nTotal cost: ${message.total_cost_usd or 'N/A'}")


asyncio.run(main())
```

---

## 4. Custom MCP Tools

Use when the workflow needs to call custom logic, APIs, or databases.

```python
import asyncio
from typing import Any
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)


# Define tools with the @tool decorator
@tool("lookup_user", "Look up a user by email address", {"email": str})
async def lookup_user(args: dict[str, Any]) -> dict[str, Any]:
    # Replace with actual database/API call
    users = {
        "alice@example.com": {"name": "Alice", "role": "admin", "active": True},
        "bob@example.com": {"name": "Bob", "role": "viewer", "active": False},
    }
    user = users.get(args["email"])
    if user:
        return {"content": [{"type": "text", "text": f"User found: {user}"}]}
    return {
        "content": [{"type": "text", "text": f"No user found for {args['email']}"}],
        "is_error": True,
    }


@tool(
    "create_ticket",
    "Create a support ticket",
    {"title": str, "description": str, "priority": str},
)
async def create_ticket(args: dict[str, Any]) -> dict[str, Any]:
    # Replace with actual ticket system API call
    ticket_id = "TICKET-12345"
    return {
        "content": [
            {
                "type": "text",
                "text": f"Created ticket {ticket_id}: {args['title']} (priority: {args['priority']})",
            }
        ]
    }


async def main():
    # Create the in-process MCP server
    support_server = create_sdk_mcp_server(
        name="support_tools",
        version="1.0.0",
        tools=[lookup_user, create_ticket],
    )

    options = ClaudeAgentOptions(
        mcp_servers={"support": support_server},
        allowed_tools=[
            "mcp__support__lookup_user",
            "mcp__support__create_ticket",
        ],
    )

    async with ClaudeSDKClient(options) as client:
        await client.query(
            "Look up the user alice@example.com and create a high-priority "
            "ticket about their account needing a password reset."
        )
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Cost: ${message.total_cost_usd or 'N/A'}")


asyncio.run(main())
```

---

## 5. Hooks for Governance

Use hooks to enforce guardrails, audit tool usage, or modify behavior.

```python
import asyncio
import json
from datetime import datetime, timezone
from typing import Any
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    HookMatcher,
    HookContext,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)


# --- Hook: Block dangerous bash commands ---
async def block_dangerous_commands(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    command = input_data.get("tool_input", {}).get("command", "")
    forbidden = ["rm -rf /", "mkfs", "dd if=", "> /dev/sda"]
    for pattern in forbidden:
        if pattern in command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Blocked dangerous pattern: {pattern}",
                }
            }
    return {}


# --- Hook: Audit log for all tool usage ---
async def audit_log(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": input_data.get("tool_name", "unknown"),
        "input_summary": str(input_data.get("tool_input", {}))[:200],
    }
    with open("agent_audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return {}


# --- Hook: Restrict file writes to certain directories ---
async def restrict_write_paths(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    # matcher="Write|Edit" already filters to these tools, so no tool_name check needed
    file_path = input_data.get("tool_input", {}).get("file_path", "")
    allowed_prefixes = ["/path/to/project/src/", "/path/to/project/tests/"]
    if not any(file_path.startswith(p) for p in allowed_prefixes):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Writes only allowed in src/ and tests/. Got: {file_path}",
            }
        }
    return {}


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[block_dangerous_commands]),
                HookMatcher(matcher="Write|Edit", hooks=[restrict_write_paths]),
                HookMatcher(hooks=[audit_log]),  # All tools
            ],
            "PostToolUse": [
                HookMatcher(hooks=[audit_log]),
            ],
        },
    )

    async for message in query(
        prompt="Clean up the codebase: remove dead code, fix linting issues, and update tests.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Cost: ${message.total_cost_usd or 'N/A'}")


asyncio.run(main())
```

---

## 6. Structured Output

Use when you need machine-readable JSON output from the agent.

```python
import asyncio
import json
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    schema = {
        "type": "object",
        "properties": {
            "files_analyzed": {"type": "integer"},
            "issues": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string"},
                        "line": {"type": "integer"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                        "description": {"type": "string"},
                    },
                    "required": ["file", "severity", "description"],
                },
            },
            "summary": {"type": "string"},
        },
        "required": ["files_analyzed", "issues", "summary"],
    }

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
        output_format={"type": "json_schema", "schema": schema},
    )

    async for message in query(
        prompt="Analyze all Python files for potential bugs and return structured results.",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            if message.result:
                results = json.loads(message.result)
                print(f"Analyzed {results['files_analyzed']} files")
                print(f"Found {len(results['issues'])} issues")
                for issue in results["issues"]:
                    print(f"  [{issue['severity']}] {issue['file']}: {issue['description']}")


asyncio.run(main())
```

---

## 7. Combined: Multi-Agent + Hooks + Custom Tools

A production-grade pattern combining multiple SDK features.

```python
import asyncio
import json
from datetime import datetime, timezone
from typing import Any
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AgentDefinition,
    HookMatcher,
    HookContext,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)


# --- Custom tools ---
@tool("notify_slack", "Send a notification to a Slack channel", {"channel": str, "message": str})
async def notify_slack(args: dict[str, Any]) -> dict[str, Any]:
    # Replace with actual Slack API call
    print(f"[Slack #{args['channel']}] {args['message']}")
    return {"content": [{"type": "text", "text": f"Notification sent to #{args['channel']}"}]}


@tool("get_deploy_status", "Check deployment status for a service", {"service": str})
async def get_deploy_status(args: dict[str, Any]) -> dict[str, Any]:
    # Replace with actual deployment API call
    return {
        "content": [
            {"type": "text", "text": f"Service {args['service']}: deployed, healthy, version 2.3.1"}
        ]
    }


# --- Hooks ---
async def cost_guard(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    """Add a system message reminding Claude to be cost-conscious."""
    return {"systemMessage": "Reminder: minimize tool calls. Batch operations when possible."}


async def log_subagent_completion(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    result = input_data.get("result", "")
    print(f"[SubagentStop] Completed. Result length: {len(result)} chars")
    return {}


# --- Main workflow ---
async def main():
    ops_server = create_sdk_mcp_server(
        name="ops",
        version="1.0.0",
        tools=[notify_slack, get_deploy_status],
    )

    options = ClaudeAgentOptions(
        allowed_tools=[
            "Read", "Write", "Edit", "Bash", "Glob", "Grep",
            "Task",  # For subagents
            "mcp__ops__notify_slack",
            "mcp__ops__get_deploy_status",
        ],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
        mcp_servers={"ops": ops_server},
        agents={
            "code-reviewer": AgentDefinition(
                description="Reviews code changes for quality, correctness, and best practices.",
                prompt="Review the code diff and provide actionable feedback.",
                tools=["Read", "Glob", "Grep"],
            ),
            "test-runner": AgentDefinition(
                description="Runs the test suite and reports results.",
                prompt="Run all tests and provide a summary of pass/fail results.",
                tools=["Bash", "Read", "Glob"],
            ),
        },
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Task", hooks=[cost_guard]),
            ],
            "SubagentStop": [
                HookMatcher(hooks=[log_subagent_completion]),
            ],
        },
    )

    async with ClaudeSDKClient(options) as client:
        await client.query(
            "Review the latest changes in src/, run the test suite, check deployment "
            "status for 'api-service', and notify #deployments with a summary."
        )
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        if block.name == "Task":
                            print(f"\n>>> Subagent: {block.input.get('description', '')}")
            elif isinstance(message, ResultMessage):
                print(f"\nTotal cost: ${message.total_cost_usd or 'N/A'}")
                print(f"Duration: {message.duration_ms}ms")
                print(f"Turns: {message.num_turns}")


asyncio.run(main())
```

---

## 8. Session Resumption and Forking

Use to continue or branch from a previous conversation.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    # First session
    session_id = None
    async for message in query(
        prompt="Analyze the project structure and create a refactoring plan.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, ResultMessage):
            session_id = message.session_id
            print(f"Session: {session_id}")

    # Resume the same session
    async for message in query(
        prompt="Now implement phase 1 of the refactoring plan you created.",
        options=ClaudeAgentOptions(
            resume=session_id,
            allowed_tools=["Read", "Write", "Edit", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, ResultMessage):
            print(f"Resumed session cost: ${message.total_cost_usd or 'N/A'}")

    # Fork the session (branch from a point without affecting the original)
    async for message in query(
        prompt="Instead, implement an alternative approach using dependency injection.",
        options=ClaudeAgentOptions(
            resume=session_id,
            fork_session=True,
            allowed_tools=["Read", "Write", "Edit", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, ResultMessage):
            print(f"Forked session: {message.session_id}")


asyncio.run(main())
```

---

## 9. Streaming Input

Use when input is generated dynamically or arrives over time.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock


async def generate_input():
    """Simulate streaming input from an external source."""
    yield {"type": "text", "text": "Here are the error logs from the last hour:\n"}
    await asyncio.sleep(0.1)
    yield {"type": "text", "text": "ERROR 10:05 - Connection timeout to database\n"}
    await asyncio.sleep(0.1)
    yield {"type": "text", "text": "ERROR 10:12 - Query failed: relation 'users' does not exist\n"}
    await asyncio.sleep(0.1)
    yield {"type": "text", "text": "\nDiagnose the root cause and suggest fixes."}


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Grep"],
        permission_mode="acceptEdits",
    )

    async for message in query(prompt=generate_input(), options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)


asyncio.run(main())
```

---

## 10. Sandboxed Execution

Use when commands should run in a restricted environment.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        permission_mode="acceptEdits",
        cwd="/path/to/project",
        sandbox={
            "enabled": True,
            "autoAllowBashIfSandboxed": True,
            "network": {
                "allowLocalBinding": True,  # Allow dev servers
            },
            "excludedCommands": ["docker"],  # Docker bypasses sandbox
        },
    )

    async for message in query(
        prompt="Build and test the project, then start a local dev server.",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            print(f"Cost: ${message.total_cost_usd or 'N/A'}")
            if message.is_error:
                print(f"Error: {message.result}")


asyncio.run(main())
```
