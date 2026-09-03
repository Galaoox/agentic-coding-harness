# ADR 0002: Progressive context and repository knowledge map

- Status: accepted
- Date: 2026-09-02

## Context

Codex v1.2 used a short skill that unconditionally loaded a 203-line orchestration contract. The OpenCode overlay also loaded one complete contract for every route. Repeated route, modifier, role, and evidence instructions consumed context even when irrelevant. Repository support declarations also drifted: `AGENTS.md` said Codex-only while architecture documented Codex and OpenCode.

## Decision

1. Treat `AGENTS.md` as a compact map containing only always-on invariants, supported runtimes, validation entrypoints, and a link to `docs/index.md`.
2. Catalog repository knowledge and context scenarios in `docs/knowledge-base.yaml`.
3. Split runtime contracts by route, evidence phase, and modifier. Load only the selected route; load `long-running` and `high-risk` only when gated.
4. Keep distributable runtime packages self-contained. Repository docs can map packages but cannot be required after installation.
5. Keep shared semantic invariants in `packages/core/`; runtime references own executable mechanics.
6. Report deterministic bytes, characters, lines, and words. Do not present character heuristics as exact model-token counts.
7. Cap Sol at `high`: use `medium` by default, Terra for everyday Standard work/exploration/verification, and Luna for mechanical strongly checked work.
8. Enforce the map, links, package boundaries, support declarations, context scenarios, and model policy in tests and CI.

## Consequences

- Direct and normal Standard tasks load substantially less Codex contract text.
- High-risk and long-running tasks deliberately load additional safeguards.
- OpenCode's previous contract was already compact; modularization primarily improves relevance and explicitness rather than guaranteeing lower size for every scenario.
- More files create navigation overhead, so references are split only on real route/modifier/phase boundaries.
- Documentation validation detects structural drift but cannot prove semantic correctness; candidate-specific execution remains authoritative.
