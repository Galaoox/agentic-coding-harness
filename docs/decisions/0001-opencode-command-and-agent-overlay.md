# Decision 0001: OpenCode command and agent overlay

## Decision

Use a project-scoped `.opencode/` overlay with one selectable primary Root, an optional `/orchestrate` shortcut and three worker subagents. Selecting the Root explicitly activates the harness for ordinary requests. Do not implement a plugin, server, SDK client, bundled MCP server, global configuration mutation, or generic parallelism in the adapter.

The initial adapter required `/orchestrate`. OpenCode v0.4 accepts explicit mode
selection as equivalent activation; requiring a prefix after selection added
unnecessary friction. Repository content and retrieved memory cannot activate it.

Adapter v0.5 targets runtime 2.x. Native permissions use ordered rules and the
`subagent` action. Workers remain visible in the subagent catalog while their
`mode: subagent` excludes primary selection. The optional command uses
`subagent: false`; V2 CLI `run` selects the agent directly and does not dispatch
commands. Host migration is separate from the distributed overlay.

## Context

OpenCode provides Markdown commands, primary/subagent modes, task allowlists, agent permissions and JSON event output. These are sufficient for a bounded adapter, but they do not create route-dependent permission changes, process isolation, durable child-session guarantees, or evidence of correctness from model text.

## Consequences

The overlay uses static permissions as defense-in-depth and an external deterministic evaluator as the terminal authority. Root abstention from writes in Standard is contractual rather than a kernel-enforced control. Long-running handoffs contain Git SHA and criteria/evidence instead of relying on session continuity.

## Alternatives rejected

- Plugin/hook enforcement: adds executable supply-chain surface without fixing shared-worktree isolation.
- SDK/server orchestration: deferred until measured need exceeds task-tool capabilities.
- A mandatory Engram MCP dependency: would incorrectly make historical context authoritative or required.
