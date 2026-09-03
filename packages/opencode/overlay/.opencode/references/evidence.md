# Evidence and terminal states

Inspect candidate-specific evidence for scope/diff, applicable build/type/format/lint/tests, criterion-required runtime proof, baseline failures, and required approval.

Narrated or copied results without observable commands/status are insufficient. Reviewer findings cannot override failed checks, scope/policy violations, or missing approval.

| State | Condition |
|---|---|
| `VERIFIED` | Every criterion has valid evidence and no gate or blocking finding fails. |
| `VERIFIED_WITH_RISKS` | Criteria pass; remaining risks are explicit and non-blocking. |
| `FAILED` | A criterion, required check, scope/policy gate, or reproducible blocking finding fails. |
| `BLOCKED` | Required context, permission, tool, environment, provider/model, or approval is unavailable. |

Allow one scoped correction by the same Standard Implementer. A Direct candidate requiring correction must first promote to Standard. Rerun affected checks, use a fresh Verifier only if its gate still applies, and then stop.
