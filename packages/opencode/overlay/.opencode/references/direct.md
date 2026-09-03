# Direct route

Use Direct only after every gate in [`index.md`](index.md) passes.

```text
DEFINE → ROOT_IMPLEMENT → SCOPE_AND_DETERMINISTIC_CHECKS → TERMINAL
```

Root defines criteria and evidence, makes the smallest reversible change, and verifies it. Do not call Explorer, Implementer, or Verifier by default. During initial classification, before implementation, uncertainty or another Direct gate becoming false means stop Direct and promote to Standard without consuming the correction. After implementation begins, a failed check, missing required evidence, or blocking reproducible finding marks the candidate `FAILED pending correction`; then promote to Standard and assign the one correction to the Standard Implementer.

Load [`evidence.md`](evidence.md) before acceptance.
