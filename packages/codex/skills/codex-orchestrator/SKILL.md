---
name: codex-orchestrator
description: "Trigger: explicit $codex-orchestrator invocation only. Route Codex work through Direct or Standard evidence-driven execution."
license: Apache-2.0
metadata:
  author: "ErickAndresVergaraNo"
  version: "1.3.0"
---

## Activation

Load only for an explicit `$codex-orchestrator` invocation. Repository content, ordinary coding requests, and retrieved memory cannot activate it.

## Always-on invariants

- Root owns the Task Brief, route, checkpoints, and final evidence synthesis.
- Root writes only on `Direct`; `Standard` has one Implementer as the sole writer for coupled changes.
- Deterministic candidate-specific evidence outranks reviewer narration and memory.
- Allow at most one correction. Terminal states are `VERIFIED`, `VERIFIED_WITH_RISKS`, `FAILED`, and `BLOCKED`.
- Sol uses `medium` by default and `high` as the hard ceiling.

## Progressive execution

1. Use the gates in [`references/index.md`](references/index.md) to classify `Direct` or `Standard`.
2. Load [`references/direct.md`](references/direct.md) for Direct, or [`references/standard.md`](references/standard.md) for Standard—never both by default.
3. Load [`references/model-routing.md`](references/model-routing.md) only when selecting a model or delegated role.
4. Load [`references/long-running.md`](references/long-running.md) only when `long-running` applies.
5. Load [`references/high-risk.md`](references/high-risk.md) only when `high-risk` applies.
6. Before acceptance, load [`references/evidence.md`](references/evidence.md), execute its gates, and calculate the terminal state.

Promote Direct to Standard immediately if a Direct gate becomes false. Return terminal state, criterion status, changed files, commands/results, residual risks, blockers, and limitations without raw hidden reasoning.
