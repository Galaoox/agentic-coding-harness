# OpenCode capability matrix — adapter v0.1

**Observed:** 2026-09-02 on OpenCode `1.18.27` installed locally with `npm install --global opencode-ai@1.18.27`. No user credentials were copied into fixtures.

| Capability | Status | Local evidence | Design consequence | Official source |
|---|---|---|---|---|
| Project Markdown agents | confirmed | `.opencode/agents/*.md` appeared in `opencode agent list` and `debug config` | Overlay uses Markdown agents | https://opencode.ai/docs/agents/ |
| Modes and hidden agents | confirmed | `cap-primary` reported primary; `cap-worker` reported subagent and hidden | Root primary, internal workers hidden | https://opencode.ai/docs/agents/ |
| Agent permissions | confirmed | `debug agent cap-worker` showed edit/bash/task disabled; debug tool calls returned disabled errors | Explorer denies edit/bash/task; Verifier denies edit/task and asks for shell except allowlist | https://opencode.ai/docs/permissions/ |
| Task allowlist | confirmed (config) | `debug agent cap-primary` showed deny-all followed by allow `cap-worker` | Root has exact allowlist of three workers | https://opencode.ai/docs/agents/ |
| `subagent_depth` | confirmed (config) | `debug config` returned `subagent_depth: 1` | Example preserves primary→worker only | https://opencode.ai/docs/config/ |
| Project commands | confirmed | `.opencode/commands/capability.md` appeared in resolved config | `/orchestrate` is explicit public entry | https://opencode.ai/docs/commands/ |
| Command selects a primary without child context | confirmed | `opencode run --command capability --format json` emitted `CAP_COMMAND_READY` with `subtask: false` | `/orchestrate` fixes primary agent and `subtask: false` | https://opencode.ai/docs/commands/ |
| JSON event stream | confirmed | run emitted `step_start`, `tool_use`, `text`, `step_finish` JSONL events | Runner parses both `tool` and `tool_use`; events remain telemetry, not correctness evidence | https://opencode.ai/docs/cli/ |
| Runtime-generated `.opencode` files | confirmed | live runs added `package.json`, `package-lock.json`, `node_modules/` and `.gitignore` beside the installed overlay | Installer owns only its manifest files; uninstall preserves foreign runtime files and docs require ignoring/reviewing them | https://opencode.ai/docs/plugins/ |
| Resumable child session | unknown | CLI/SDK surface not exercised with a real nested task | long-running uses SHA/progress handoff, not durable child resume | https://opencode.ai/docs/sdk/ |
| Dynamic route permissions | unsupported | route is prompt/runtime state, while permissions are static agent config | Standard Root non-writing boundary is process policy, not sandbox | https://opencode.ai/docs/permissions/ |

## Exact local probes

- `opencode --version` → `1.18.27`
- `opencode run --help` exposes `--command`, `--agent`, `--format json`.
- `opencode debug config` resolved project command and agents.
- `opencode debug agent cap-worker --tool edit ...` → `Tool edit is disabled for agent cap-worker`.
- `opencode debug agent cap-worker --tool bash ...` → `Tool bash is disabled for agent cap-worker`.

The capability fixture returned model output for simple commands. Its provider identity is intentionally not captured; `opencode providers list` reported zero configured user credentials in the process environment. That proves command/agent execution, not that an external provider is configured for portable CI.
