# Repository instructions

## Scope

This repository develops reusable agentic coding workflows. Codex is the only supported runtime in the current milestone. Do not add OpenCode or other runtime adapters unless the task explicitly requests that work.

## Working agreements

- Keep runtime-neutral contracts under `packages/core/`.
- Keep Codex-specific behavior under `packages/codex/`.
- Preserve explicit invocation for orchestration skills unless a task changes that policy.
- Route work by uncertainty, risk, coupling, and verifiability. Do not use file counts as a proxy for complexity.
- Prefer executable evidence over agent narration.
- Treat retrieved memory as historical context that must be checked against current sources.
- Keep required rules in versioned files, not only in memory systems.
- Do not add dependencies or generated artifacts without a concrete need.
- Use conventional commits. Do not add AI attribution.
