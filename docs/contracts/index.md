# Contract catalog

The canonical contract is [`../../packages/core/contracts/evidence-driven-orchestration.md`](../../packages/core/contracts/evidence-driven-orchestration.md). It owns runtime-neutral routing, optional planning, continuity, investigation, reproduction, evidence, one writer, three corrections per independent root defect, and terminal states.

Runtime packages own only their executable mechanics:

- [Codex runtime map](../runtimes/codex.md)
- [OpenCode runtime map](../runtimes/opencode.md)

Package references must be self-contained after installation. They may summarize shared invariants required for safe execution, but repository-only links are not runtime dependencies.

## Contract-only scope

This update defines the shared target, not adapter parity. Codex v1.3 and OpenCode v0.2 distributables, installers, invocation, models, permissions, and runtime context scenarios remain unchanged. Their existing static assertions describe shipped behavior; passing them does not prove the new contract is implemented. Future adapter changes require candidate-specific executable evidence and separately authorized scope.

The local OpenCode workflow was inspected and backed up on 2026-10-03: `agentic-harness` version `0.7.0-local.1`, based on upstream adapter `0.2.0` at `d9f09c31b596f17781bf609f88509c50a13ec741`. The snapshot preserves 27 files across that complete workflow and `controlled-technical-writing`, including their runtime dependencies and original manifest. Five agent files differ from the original manifest; current bytes, not old hashes, are the recovery source. The writing skill is backup-only and introduces no shared mandate or activation.

## Local workflow comparison

| Area | Inspected local OpenCode workflow | Shipped repository OpenCode adapter |
|---|---|---|
| Entry and scope | Global skill; selected `agentic-harness-root` or `/agentic-harness` | Project overlay; explicit `/orchestrate` only |
| Investigation | Explorer or Researcher; one exceptional independent premise check | One gated Explorer |
| Planning | Optional compact ExecPlan; readiness and authorization separated; Root maintains it | Task Brief and concise continuity checkpoints |
| Reproduction and evidence | Recommended/mandatory RED distinction; no-edit verification batches | Criterion evidence without those detailed policies |
| Browser and permissions | Browser reference, workspace-aware permission plugin, personal external-root/Obsidian exceptions | Static permissions; no browser reference or personal exceptions |
| Correction limit | One total correction | One total correction |
| Models | Actual agents use Sol medium/high and Luna low; upstream model notes are stale | Provider/model neutral |

Local files supply evidence and useful behavior, not automatic authority for the shared target. Personal paths, trusted-root exceptions, Obsidian tooling, provider settings, global configuration, credentials, and temporary logs are not imported. Tool-specific browser and permission mechanics remain adapter concerns.

## Adapter conformance gaps

| Shared target | Codex v1.3 / OpenCode v0.2 shipped behavior | Remaining work |
|---|---|---|
| Three corrections per independent root defect; causal identity, before/after evidence, scoped stopping | One correction total; no root-defect ledger | Implement budget continuity and required-defect terminal gates; detection excluded |
| Direct escalates when its gates fail, not for a bounded error alone | Post-edit failure promotes to Standard | Align reclassification and correction ownership |
| Cross-session continuity on either route; authorized checkpoints only | Long-running modifies Standard; unit count can activate it; checkpoint when possible | Align modifier gates and authorization |
| Optional plans, readiness separate from execution, current-state reconciliation | No complete shared planning contract in either adapter | Map plan ownership and handoff without universal paths/templates |
| Recommended reproduction unless explicit RED/TDD; immutable verification batches | No detailed equivalent in either adapter | Propagate testing mode and candidate-state evidence |
| Exceptional independent read-only premise check; deterministic browser acceptance | No complete equivalent in either adapter | Map existing actors/tools and validate limits without mandatory new dependencies |

Keep adapter versions and capability claims at their shipped baseline until those changes are implemented and verified. Neither the backup nor documentation/static tests constitute runtime behavioral proof.
