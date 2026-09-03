# Evidence gates and terminal states

Before calculating a terminal state, inspect candidate-specific evidence for:

1. scope and diff;
2. applicable build, type, format, lint, and focused tests;
3. integration, E2E, runtime, UI, API, log, or database proof required by a criterion;
4. baseline failures;
5. required human approval for irreversible or external effects.

A result is valid only when tied to the candidate state and includes an observable command, status, or inspection. Reviewer opinion and copied narration cannot override missing or failed evidence.

| State | Condition |
|---|---|
| `VERIFIED` | Every required criterion has valid evidence; no gate or blocking finding fails. |
| `VERIFIED_WITH_RISKS` | Criteria have valid evidence; remaining risks are explicit and non-blocking. |
| `FAILED` | A criterion, policy/scope gate, required check, or reproducible blocking finding fails. |
| `BLOCKED` | Required context, permission, tool, environment, model, or approval is unavailable. |

## Correction

Allow one scoped correction by the same Standard Implementer. A Direct candidate requiring correction must first promote to Standard. Re-run affected deterministic checks and use a fresh Verifier only if its gate still applies. Stop after that correction; do not convert `FAILED` or `BLOCKED` into success through narration.
