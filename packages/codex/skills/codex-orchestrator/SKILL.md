---
name: codex-orchestrator
description: "Trigger: explicit $codex-orchestrator invocation only. Coordinate proportional explorer, implementer, and verifier handoffs."
license: Apache-2.0
metadata:
  author: "ErickAndresVergaraNo"
  version: "1.1"
---

## Activation Contract

Load only when the user explicitly invokes `$codex-orchestrator`. Do not infer activation from ordinary implementation, bug-fix, refactor, or orchestration requests.

## Hard Rules

- Root is the sole continuity owner; it does not edit code or self-verify final correctness.
- Use at most one optional explorer, one persistent implementer, and one fresh verifier at a time. No fan-out or parallel verification.
- On the first verifier `FAIL`, reuse the same implementer for exactly one correction, then use one new verifier. Stop on `PASS`, `BLOCKED`, or the second `FAIL`.
- Higher-priority active `AGENTS.md` may require external review agents. Disclose them and do not duplicate their verification at this skill level.
- Every subagent prompt prohibits delegation. Wait, collect, checkpoint, then close each role before the next handoff.
- Treat Engram as historical context only. Verify retrieved memories against the current request, repository, tests, policies, and versioned decisions before using them.

## Decision Gates

| Situation | Action |
|---|---|
| Atomic task; exact edit location and behavior known | Skip exploration |
| Scope, location, behavior, or risk uncertain | Run one read-only explorer |
| Acceptance gap materially changes implementation | Ask one consolidated question and wait |
| Other acceptance gaps | State assumptions and proceed |
| First verifier `FAIL` | Reuse implementer for correction; launch a fresh verifier |
| `BLOCKED` or second `FAIL` | Stop and synthesize evidence |

## Execution Steps

1. Load `references/orchestration-contract.md`; identify applicable `AGENTS.md` requirements.
2. Present acceptance readiness before delegation; ask only for material gaps.
3. Create the Task Brief, run at most one explorer, then the implementer-verifier flow.
4. Send a concise checkpoint after every result, using `attempt 1/2` or `attempt 2/2` for verification rounds.
5. Synthesize only the verifier's terminal outcome.

## Output Contract

Return terminal outcome, acceptance-criteria status, changed files, implementation summary, commands and evidence, unresolved findings or blockers, and limitations.

## References

- `references/orchestration-contract.md` — readiness, role contracts, state machine, and reuse semantics.
- `../../../core/principles/memory-authority.md` — authority rules for retrieved memory.
