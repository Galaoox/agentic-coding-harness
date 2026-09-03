# Repository knowledge map

This directory is the repository knowledge base. `AGENTS.md` is the compact entrypoint; this index maps tasks to deeper sources of truth. Load only what the current task needs.

## Normative sources

| Need | Source |
|---|---|
| Architecture and runtime boundaries | [`architecture.md`](architecture.md) |
| Shared orchestration invariants | [`../packages/core/contracts/evidence-driven-orchestration.md`](../packages/core/contracts/evidence-driven-orchestration.md) |
| Retrieved-memory authority | [`../packages/core/principles/memory-authority.md`](../packages/core/principles/memory-authority.md) |
| Contract catalog | [`contracts/index.md`](contracts/index.md) |
| Codex runtime map | [`runtimes/codex.md`](runtimes/codex.md) |
| OpenCode runtime map | [`runtimes/opencode.md`](runtimes/opencode.md) |
| Machine-readable knowledge/context catalog | [`knowledge-base.yaml`](knowledge-base.yaml) |

## Decision and evidence records

- [`decisions/`](decisions/) contains architectural decisions.
- [`evaluation/`](evaluation/) contains smoke cases and observed results; evidence is historical until reproduced against the current candidate.
- [`research/`](research/) contains capability reconnaissance and external-runtime findings.
- [`baselines/`](baselines/) preserves superseded package baselines.

## Planning

Repository execution plans belong under `docs/plans/active/` while active and `docs/plans/completed/` after completion when they need to be shared and versioned. Local Hermes plans under `.hermes/` are not product documentation and are not committed by default.

## Authority

Current user requirements and candidate-specific executable evidence outrank this documentation. Normative documents outrank historical evaluation and research. If two normative sources disagree, stop, record the conflict, and fix the source-of-truth map before relying on either.
