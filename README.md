# Agentic Coding Harness

A Codex-first monorepo for adaptive, evidence-driven software-development workflows.

The project starts with Codex. Support for other runtimes, such as OpenCode, is a future extension and is not part of the current implementation.

## Principles

- Route work by uncertainty, risk, coupling, and verifiability.
- Keep one implementation owner for coupled changes.
- Prefer executable evidence over agent narration.
- Use fresh review only for residual risks.
- Use Engram to recover the past, never to decide the present.
- Keep required rules and authoritative decisions in versioned repository files.

## Repository layout

```text
packages/
  core/                         Shared contracts and runtime-neutral principles
  codex/
    skills/
      codex-orchestrator/       Initial Codex workflow
docs/
  architecture.md              Boundaries and extension strategy
```

## Status

Experimental. The first milestone is to replace the fixed explorer–implementer–verifier topology with proportional execution routes for Codex.

## License

Apache-2.0
