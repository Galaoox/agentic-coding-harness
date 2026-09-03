# Contract catalog

The shared contract is [`../../packages/core/contracts/evidence-driven-orchestration.md`](../../packages/core/contracts/evidence-driven-orchestration.md). It owns runtime-neutral route, modifier, evidence, writer, correction, and terminal-state invariants.

Runtime packages own only their executable mechanics:

- [Codex runtime map](../runtimes/codex.md)
- [OpenCode runtime map](../runtimes/opencode.md)

Package references must be self-contained after installation. They may summarize shared invariants required for safe execution, but repository-only links are not runtime dependencies.
