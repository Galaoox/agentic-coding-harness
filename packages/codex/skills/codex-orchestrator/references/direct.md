# Direct route

Use Direct only after every gate in [`index.md`](index.md) passes.

```text
DEFINE → ROOT_IMPLEMENT → SCOPE_AND_DETERMINISTIC_CHECKS → TERMINAL
```

Root records concise acceptance criteria and a `criterion → evidence` matrix, implements the smallest reversible change, and runs applicable checks. Explorer, Implementer, and Verifier are omitted by default.

During initial classification, before implementation, uncertainty, material risk, an unresolved decision, or insufficient prospective deterministic coverage means stop Direct and promote to Standard without consuming the correction. After implementation begins, a failed check, missing required evidence, or blocking reproducible finding marks the candidate `FAILED pending correction`; then promote to Standard and assign the one correction to the Standard Implementer. Direct never carries `high-risk` or `long-running`.

Before acceptance, load [`evidence.md`](evidence.md).
