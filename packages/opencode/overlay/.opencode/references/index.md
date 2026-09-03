# OpenCode orchestration reference map

This installed overlay is self-contained. Treat OpenCode permissions as defense-in-depth, not sandboxing; `hidden: true` is UX only and hidden agents remain manually invocable. JSONL events are telemetry, not correctness evidence.

## Task Brief and authority

Before editing or delegation, Root records a concise Task Brief with the intended outcome and non-goals, assumptions and constraints, stable criterion IDs, a criterion-to-evidence matrix, candidate state (base SHA, working tree, and relevant baseline failures), route and modifiers, and escalation conditions.

Authority descends from the current request and acceptance criteria, through candidate code and executed evidence, applicable policies and versioned documentation, to Git/issue context, retrieved memory, and finally agent narration. If memory materially influences the brief, record the memory source and the higher-authority current evidence that confirms or refutes it.

Ask one consolidated question only when missing information materially changes scope, implementation, validation, safety, or an irreversible effect; otherwise record an assumption and proceed. After each role or evidence gate, checkpoint only `Completed`, `Status`, `Progress`, and `Next`.

## Route gates

Select Direct only when all hold:

1. Outcome and acceptance criteria are unambiguous.
2. Edit location is known after short Root inspection.
3. No architecture, compatibility, security, or data decision remains.
4. Change is low-risk, reversible, and not high-risk.
5. Deterministic evidence can cover every criterion.

Otherwise select Standard.

## Conditional map

| Condition or phase | Load |
|---|---|
| Direct selected | [`direct.md`](direct.md) |
| Standard selected | [`standard.md`](standard.md) |
| long-running applies | [`long-running.md`](long-running.md) |
| high-risk applies | [`high-risk.md`](high-risk.md) |
| Before terminal acceptance | [`evidence.md`](evidence.md) |

`long-running` and `high-risk` modify Standard; they are not routes. Do not preload the opposite route or unused modifiers.
