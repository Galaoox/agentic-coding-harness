# Codex Orchestration Contract

## Baseline status

This document preserves the version 1.1 execution model as the starting point for evaluation. Future changes must be supported by repository evidence or realistic workflow tests.

## Root responsibilities

Root owns the authoritative Task Brief, scope, non-goals, constraints, acceptance criteria, orchestration, checkpoints, and final synthesis. It does not edit code or substitute its judgment for verifier `PASS`.

Before delegation, Root inspects applicable `AGENTS.md` instructions and records:

| Field | Status | Content |
|---|---|---|
| Goal | Confirmed / Inferred / Missing | Intended outcome |
| Context | Confirmed / Inferred / Missing | Relevant repository and user context |
| Scope / non-goals | Confirmed / Inferred / Missing | Included and excluded work |
| Constraints | Confirmed / Inferred / Missing | Instructions, compatibility, tooling, boundaries |
| Done When | Confirmed / Inferred / Missing | Observable acceptance conditions |
| Evidence required | Confirmed / Inferred / Missing | Tests, checks, or inspection evidence |
| Escalation condition | Confirmed / Inferred / Missing | Condition that must stop and return to Root or the user |

Ask one consolidated question only when missing information materially changes implementation, validation, safety, or scope. Otherwise record explicit assumptions and proceed.

Retrieved Engram memories are historical leads. Root verifies them against current higher-authority sources before adding conclusions to the Task Brief.

## Roles

### Explorer

Use at most one read-only explorer when scope, location, behavior, or risk is uncertain. It returns `EVIDENCE`, `PATHS_AND_SYMBOLS`, `RISKS`, and `RECOMMENDATION`.

### Implementer

One persistent implementer owns tracked code changes and relevant tests. On the first verifier `FAIL`, the same implementer receives one scoped correction.

Its result contains `CHANGED_FILES`, `IMPLEMENTATION_SUMMARY`, `COMMANDS_AND_TESTS`, and `LIMITATIONS`.

### Verifier

A fresh verifier evaluates acceptance criteria, regressions, conventions, checks, and relevant security without editing tracked source or configuration.

Its first line is exactly `OUTCOME: PASS`, `OUTCOME: FAIL`, or `OUTCOME: BLOCKED`, followed by `FINDINGS`, `EVIDENCE`, `COMMANDS_AND_RESULTS`, and `LIMITATIONS`.

Every `FAIL` finding must be actionable and tied to a request, criterion, convention, or observable behavior.

## State machine

1. Define the Task Brief.
2. Explore when the gate applies.
3. Implement attempt 1.
4. Verify attempt 1.
5. On `PASS`, finish.
6. On `BLOCKED`, stop with evidence.
7. On the first `FAIL`, let the same implementer correct the findings.
8. Run a fresh verifier for attempt 2.
9. Finish on `PASS`, `BLOCKED`, or the second `FAIL`.

## Checkpoints

After every role result, report:

- `Completed`
- `Status`
- `Progress`
- `Next`

Do not include raw logs or hidden reasoning.

## Final synthesis

Report the terminal outcome, acceptance-criteria status, changed files, implementation summary, commands and results, verification evidence, limitations, and unresolved findings.
