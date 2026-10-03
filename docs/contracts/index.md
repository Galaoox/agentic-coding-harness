# Contract catalog

The canonical contract is [`../../packages/core/contracts/evidence-driven-orchestration.md`](../../packages/core/contracts/evidence-driven-orchestration.md). It owns runtime-neutral routing, optional planning, continuity, investigation, reproduction, evidence, one writer, three corrections per independent root defect, and terminal states.

Runtime packages own only their executable mechanics:

- [Codex runtime map](../runtimes/codex.md)
- [OpenCode runtime map](../runtimes/opencode.md)

Package references must be self-contained after installation. They may summarize shared invariants required for safe execution, but repository-only links are not runtime dependencies.

## Contract history

The prior contract-only update left Codex v1.3 and OpenCode v0.2 unchanged. Codex v1.4 and OpenCode v0.3 now specify the six shared capability groups below. Static validation still does not prove runtime model behavior.

The local OpenCode workflow was inspected and backed up on 2026-10-03: `agentic-harness` version `0.7.0-local.1`, based on upstream adapter `0.2.0` at `d9f09c31b596f17781bf609f88509c50a13ec741`. The snapshot preserves 27 files across that complete workflow and `controlled-technical-writing`, including their runtime dependencies and original manifest. Five agent files differ from the original manifest; current bytes, not old hashes, are the recovery source. The writing skill is backup-only and introduces no shared mandate or activation.

## Historical local workflow comparison

| Area | Inspected local OpenCode workflow | Previous repository OpenCode v0.2 adapter |
|---|---|---|
| Entry and scope | Global skill; selected `agentic-harness-root` or `/agentic-harness` | Project overlay; explicit `/orchestrate` only |
| Investigation | Explorer or Researcher; one exceptional independent premise check | One gated Explorer |
| Planning | Optional compact ExecPlan; readiness and authorization separated; Root maintains it | Task Brief and concise continuity checkpoints |
| Reproduction and evidence | Recommended/mandatory RED distinction; no-edit verification batches | Criterion evidence without those detailed policies |
| Browser and permissions | Browser reference, workspace-aware permission plugin, personal external-root/Obsidian exceptions | Static permissions; no browser reference or personal exceptions |
| Correction limit | One total correction | One total correction |
| Models | Actual agents use Sol medium/high and Luna low; upstream model notes are stale | Provider/model neutral |

Local files supply evidence and useful behavior, not automatic authority for the shared target. Personal paths, trusted-root exceptions, Obsidian tooling, provider settings, global configuration, credentials, and temporary logs are not imported. Tool-specific browser and permission mechanics remain adapter concerns.

## Adapter conformance

| Shared capability | Previous v1.3 / v0.2 behavior | v1.4 / v0.3 specification |
|---|---|---|
| Three corrections per independent root defect; causal identity, before/after evidence, scoped stopping | One correction total; no root-defect ledger | Budgets persist across actors/routes/sessions; detection excluded; unresolved required defects stop dependent work |
| Direct escalates when its gates fail, not for a bounded error alone | Post-edit failure promotes to Standard | Reclassify only when a Direct gate fails; preserve causal correction ownership |
| Cross-session continuity on either route; authorized checkpoints only | Long-running modifies Standard; unit count can activate it; checkpoint when possible | Continuity applies to either route; Git checkpoints require authorization |
| Optional plans, readiness separate from execution, current-state reconciliation | No complete shared planning contract in either adapter | Root maintains optional plans; reconcile current evidence before accepting a handoff |
| Recommended reproduction unless explicit RED/TDD; immutable verification batches | No detailed equivalent in either adapter | Carry testing mode; stop verification on candidate mutation; tie checks to candidate identity |
| Exceptional independent read-only premise check; deterministic browser acceptance | No complete equivalent in either adapter | Bound the premise check; require assertions for browser acceptance; no mandatory new dependencies |

The behaviors described in the last column are now specified in both self-contained reference sets. The catalog marks each capability `specified` with model-backed conformance `pending`. Evaluate current behavior using the [smoke guide](../evaluation/harness-smoke-guide.md); do not infer full parity from static tests or one passing outcome. The local backup and writing skill retain their historical scope.
