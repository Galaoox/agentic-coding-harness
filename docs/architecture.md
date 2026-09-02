# Architecture

## Purpose

The monorepo separates runtime-neutral workflow contracts from runtime integrations.

```text
packages/
  core/
    principles/
  codex/
    skills/
```

## Current boundary

Codex is the only supported runtime. The repository may add adapters for OpenCode or other systems later, but current contracts must not depend on unimplemented adapters.

## Design direction

The current `codex-orchestrator` skill is preserved as a baseline. Future revisions will evaluate an adaptive topology with proportional routes:

- atomic;
- normal;
- complex or long-running;
- high-risk.

Each change to the workflow should be supported by a realistic task, observed failure, or evaluation result. Avoid adding roles, review passes, documents, or protocol states only for theoretical completeness.

## Authority model

Current evidence has precedence over historical memory:

1. Current user request and acceptance criteria.
2. Current code, configuration, and executable tests.
3. Versioned repository policies and documentation.
4. Current ADRs and recorded decisions.
5. Git history and issue context.
6. Retrieved memory.

Memory can locate relevant history. It cannot authorize a present decision without verification.

## Extension strategy

A future runtime integration should implement shared contracts without changing their semantics. Runtime-specific configuration, prompts, transport, and lifecycle behavior belong in that runtime's package.
