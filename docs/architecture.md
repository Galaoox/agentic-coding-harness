# Architecture

## Purpose

The monorepo separates runtime-neutral workflow principles from runtime integrations.

```text
packages/
  core/
    contracts/
    principles/
  codex/
    skills/
  opencode/
    overlay/.opencode/
    install/
```

## Runtime boundaries

Codex v1.2 and OpenCode v0.1 are supported runtime adapters. `packages/core/contracts/evidence-driven-orchestration.md` contains only shared invariants: Direct/Standard routing, modifiers, evidence authority, one writer, one correction and terminal states. Runtime packages own their activation, agent/tool configuration, permissions, lifecycle semantics and installation.

## Codex v1.2 design

`packages/codex/skills/codex-orchestrator` defines one Codex-specific, explicitly invoked orchestration contract:

```text
Direct
  DEFINE → ROOT_IMPLEMENT → DETERMINISTIC_CHECKS → TERMINAL

Standard
  DEFINE → EXPLORE? → IMPLEMENT → DETERMINISTIC_CHECKS → REVIEW? → TERMINAL
                 + long-running?
                 + high-risk?
```

`Direct` is permitted only when outcome, edit location, risk and deterministic evidence are clear. Root may write only on this route. Any uncertainty promotes work to `Standard`.

`Standard` keeps one tracked-change owner. Explorer and Verifier are gated, not default stages. `long-running` and `high-risk` modify Standard safeguards without creating separate role graphs or state machines.

The authoritative implementation details remain in `packages/codex/skills/codex-orchestrator/references/orchestration-contract.md`; this document intentionally does not duplicate every gate.

## OpenCode v0.1 design

`packages/opencode/overlay/.opencode` provides `/orchestrate`, a primary `harness-orchestrator`, and hidden `harness-explorer`, `harness-implementer`, and `harness-verifier` subagents. The overlay is installed per project; it does not mutate global config or select a provider/model.

OpenCode permissions are static defense-in-depth, not sandboxing. In particular, a Standard Root's non-writing role is contractual, and any agent granted shell could write unless shell is also constrained. Explorer denies shell entirely; Verifier accepts only an approval-gated shell allowlist. The runner uses JSONL only as audit telemetry and gives authority to external deterministic evidence.

The adapter was capability-tested on OpenCode 1.18.27. The exact observed behavior and unsupported assumptions are in `docs/research/opencode-capability-matrix.md`.

## Evidence authority

Current evidence has precedence over historical memory and agent opinion:

1. Current user request and acceptance criteria.
2. Current candidate code, configuration, and executable evidence.
3. Versioned repository policies and documentation.
4. Versioned decisions.
5. Git history and issue context.
6. Retrieved memory.
7. Agent narration and opinion.

Memory can locate relevant history. It cannot authorize a present decision without verification. Likewise, reviewer output supplies findings but cannot override failed deterministic checks, scope/policy violations, missing evidence, or a blocked required approval.

## Extension strategy

A future runtime integration should reuse only stable, evidence-oriented principles from `packages/core`. Runtime-specific prompts, tool semantics, metadata, lifecycle behavior, and installation remain in the runtime package. Do not promote the Codex v1.2 state model into a universal adapter until a second concrete runtime demonstrates that abstraction is necessary.
