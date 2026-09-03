# Codex Orchestrator v1.1 baseline

This document preserves the pre-v1.2 workflow for comparison. Its source is commit [`dbc3b40d2ab44f215d6b6d0b6ddfc2581874eebf`](https://github.com/Galaoox/agentic-coding-harness/tree/dbc3b40d2ab44f215d6b6d0b6ddfc2581874eebf).

## Topology

```text
Root → Explorer (optional) → Implementer → fresh Verifier
                              ↑               │
                              └── one retry ──┘
```

- Root did not edit code or self-verify final correctness.
- One optional read-only Explorer, one persistent Implementer, and one fresh Verifier were allowed at a time.
- The topology was effectively mandatory for implementation work after optional exploration.
- The first verifier `FAIL` triggered exactly one correction by the same Implementer and a fresh second verifier.
- The workflow ended on verifier `PASS`, `BLOCKED`, or the second `FAIL`.

## Preserved strengths

- One writer owned coupled changes.
- Exploration was read-only and limited.
- Verification used a fresh context.
- Retries were bounded.
- Engram was explicitly historical context requiring current verification.

## Limitations addressed by v1.2

- Direct, fully specified fixes still paid for a multi-agent flow.
- Verifier `PASS` acted as terminal authority without an explicit acceptance-to-evidence matrix.
- Deterministic checks and LLM review were not separated strongly enough.
- Long-running and high-risk work had no bounded modifier contract.
- Baseline failures and reviewer residual risks were not first-class terminal-state inputs.

v1.2 keeps the bounded ownership and retry discipline while limiting delegation to uncertainty and residual risk.
