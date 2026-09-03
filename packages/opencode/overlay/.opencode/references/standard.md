# Standard route

```text
DEFINE → EXPLORE? → IMPLEMENT → SCOPE_AND_DETERMINISTIC_CHECKS → REVIEW? → TERMINAL
```

- Root does not edit implementation files.
- `harness-explorer` is optional, read-only, and used only when location, behavior, dependencies, or risk are uncertain.
- `harness-implementer` is the single writer for coupled source, configuration, and tests. It cannot delegate.
- `harness-verifier` is fresh and read-only. Use it only for high-risk, unresolved material API/architecture risk, insufficient deterministic coverage, or a concrete residual risk.

Run roles serially. No writer fan-out. Every delegated task prohibits further delegation. One correction may return to the same Implementer for blocking reproducible findings.

Load modifier references only when gated, then [`evidence.md`](evidence.md) before acceptance.
