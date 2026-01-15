---
trigger: always_on
---

# MCP Scope & Secrets Guardrail (ALWAYS ON)

## Purpose
This rule imposes boundaries and security when the Agent uses tools (MCP) and the filesystem.

## Workspace Scope (MANDATORY)
- Consider ONLY the root of the open workspace as "allowed root".
- **INTERRUPT**: If an operation requires exiting the workspace, the Agent **MUST STOP** and ask for explicit motivated confirmation.

## Secrets & Sensitive Files (ABSOLUTE PROHIBITION)
The Agent **MUST NEVER** read, print, or search for content in:
- Any `.env*` file (`.env`, `.env.local`, etc.)
- `**/mcp_secrets.env`
- `~/.ssh/**`, `**/id_rsa*`, `**/known_hosts`
- `**/secrets/**`, `**/*token*`, `**/*apikey*`, `**/*key*`

## MCP Usage: Operational Rules
- Use `sequential-thinking` to plan every non-trivial task.
- Use `brave-search` ONLY when external info is needed.
- Use "context7" when real validated docs are needed.
- Do not invent: if you don't find it, declare it and propose the next step.

## Terminal Safety
- If a command is not in the Allow List, always request review (approval).
- **INTERRUPT**: Do not propose destructive commands (`rm`, `sudo`, `chmod -R`, etc.) without a detailed plan and explicit confirmation.