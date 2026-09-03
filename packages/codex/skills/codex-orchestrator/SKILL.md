---
name: codex-orchestrator
description: "Trigger: explicit $codex-orchestrator invocation only. Route Codex work through Direct or Standard evidence-driven execution."
license: Apache-2.0
metadata:
  author: "ErickAndresVergaraNo"
  version: "1.2.0"
---

## Activation Contract

Load only when the user explicitly invokes `$codex-orchestrator`. Do not infer activation from ordinary implementation, bug-fix, refactor, or orchestration requests.

## Hard Rules

- Root owns continuity, the Task Brief, routing, checkpoints, and final evidence synthesis.
- Root may edit only on the `Direct` route. `Standard` has one persistent Implementer as the sole tracked-change owner.
- Use at most one read-only Explorer and one fresh Verifier at a time. v1.2 is serial: no writer fan-out or parallel verification.
- Run deterministic checks before any review gate. A reviewer finding cannot override a failed check, missing required evidence, or current higher-authority instruction.
- Retain at most one correction: after a blocking, reproducible finding, the same Implementer corrects once and a fresh Verifier reviews again only when the review gate still applies. Stop on `VERIFIED`, `VERIFIED_WITH_RISKS`, `FAILED`, or `BLOCKED`.
- Every delegated prompt prohibits further delegation. Wait, collect, checkpoint, and close each role before the next handoff.
- Treat Engram as historical context only. Verify retrieved memories against the current request, repository, tests, policies, and versioned decisions before using them.

## Route Gates

| Route or modifier | Use when | Required behavior |
|---|---|---|
| `Direct` | All five Direct gates in the contract hold | Root implements and verifies directly. |
| `Standard` | Any Direct gate fails or becomes uncertain | Optional Explorer, one Implementer, deterministic checks, then a gated review. |
| `long-running` | Standard needs several independently verifiable units or session handoff | Add checkpoints and concise versioned progress state. |
| `high-risk` | Auth, money, migrations, secrets, PII, concurrency, infrastructure, or irreversible effects are involved | Add baseline, rollback, relevant negative checks, isolated environment when viable, fresh Verifier, and human approval for irreversible/external effects. |

Promote `Direct` to `Standard` immediately if uncertainty or material risk appears. Do not keep editing under a Direct classification after promotion.

## Execution Steps

1. Load `references/orchestration-contract.md`; inspect applicable `AGENTS.md` requirements and the current candidate state.
2. Define acceptance criteria and the `criterion → evidence` matrix. Ask one consolidated question only for material gaps; otherwise state assumptions.
3. Select `Direct` or `Standard`, then apply `long-running` and/or `high-risk` only when their gates hold.
4. Execute the selected route. Run scope inspection and deterministic checks before deciding whether residual-risk review is required.
5. Calculate the terminal state from acceptance evidence, policy/scope gates, and reproducible findings. Do not synthesize a reviewer `PASS` as authority.
6. Return terminal state, criterion status, changed files, commands and results, residual risks, blockers, and limitations.

## References

- `references/orchestration-contract.md` — normative gates, role contracts, evidence model, state machine, and retry semantics.
- `../../../core/principles/memory-authority.md` — authority rules for retrieved memory.
