# Codex Orchestration Contract v1.2

## Purpose and authority

This is the normative contract for `codex-orchestrator` v1.2. It replaces the fixed v1.1 `Explorer → Implementer → Verifier` topology with a bounded routing model. It does not add a runtime-neutral adapter, parallel writers, or an autonomous retry loop.

Authority is ordered as follows:

1. Current request and acceptance criteria.
2. Current candidate code/configuration and executed evidence.
3. Applicable versioned policies and instructions.
4. Versioned decisions and documentation.
5. Git and issue context.
6. Retrieved memory, including Engram.
7. Agent narration or opinion.

A memory is a lead, not a decision. A reviewer is a source of findings, not a terminal authority.

## Task Brief and evidence matrix

Before editing or delegation, Root records a concise Task Brief:

| Field | Required content |
|---|---|
| Request | Intended observable outcome |
| Goal / non-goals | Included behavior and prohibited scope expansion |
| Assumptions | Explicit inferences that do not require a user decision |
| Constraints | Applicable instructions, compatibility, tooling, security, and boundaries |
| Acceptance criteria | Stable IDs and observable pass conditions |
| Evidence matrix | For each criterion: command, inspection, runtime proof, or justified limitation |
| Candidate state | Base SHA, working-tree state, and baseline failures where relevant |
| Route / modifiers | `Direct` or `Standard`; optional `long-running` / `high-risk` |
| Escalation | Conditions requiring Root or user action |

Ask one consolidated question only when missing information materially changes scope, implementation, validation, safety, or an irreversible effect. Otherwise state the assumption and proceed.

## Routes

### Direct

Root selects `Direct` only when **all** gates hold:

1. Requested behavior and expected outcome are unambiguous.
2. The edit location is known or discoverable by a short Root inspection.
3. No unresolved architecture, compatibility, security, or data decision remains.
4. The change is low-risk, reversible, and not `high-risk`.
5. Deterministic checks can provide sufficient evidence for every acceptance criterion.

Flow:

```text
DEFINE → ROOT_IMPLEMENT → SCOPE_AND_DETERMINISTIC_CHECKS → TERMINAL
```

Root owns edits and checks. Explorer, Implementer, and Verifier are omitted by default. If a Direct gate becomes false, Root stops the Direct flow and promotes the task to Standard before continuing.

### Standard

Use `Standard` whenever any Direct gate is false or uncertain.

```text
DEFINE → EXPLORE (only when uncertain) → IMPLEMENT → SCOPE_AND_DETERMINISTIC_CHECKS → REVIEW (only when gated) → TERMINAL
```

- Explorer is optional, read-only, and used only for uncertainty about scope, location, behavior, dependencies, or risk.
- One persistent Implementer owns all coupled tracked changes and relevant tests.
- Root does not edit Standard implementation files except to resolve an explicit orchestration artifact such as the Task Brief or progress state.
- Run serially in v1.2. No fan-out, parallel writers, or simultaneous reviews.

## Modifiers

### `long-running`

Apply only to Standard when the task requires multiple independently verifiable units or must survive a context/session boundary.

For each unit:

1. Define unit acceptance criteria.
2. Implement and execute deterministic checks.
3. Create a Git checkpoint or record why a checkpoint is not possible.
4. Update a concise versioned progress artifact only when a later session needs it.
5. Handoff base/candidate SHA, completed criteria, evidence, unresolved risks, and exactly one next unit.

Do not add roles or automatically reset context merely because the modifier applies.

### `high-risk`

Apply only to Standard for authentication/authorization, money, data migrations, secrets, PII, concurrency, infrastructure, production changes, or destructive/irreversible effects.

Required additions:

- baseline or pre-change evidence;
- rollback approach;
- isolated environment when viable;
- relevant positive and negative checks;
- a fresh Verifier after deterministic checks;
- explicit human approval before irreversible or external side effects.

A high-risk reviewer cannot authorize failed checks, scope violations, or absent human approval.

## Roles and result contracts

### Root

Root owns acceptance, routing, state, checkpoints, and final synthesis. Root can implement only Direct. It treats Engram and all agent reports as evidence to verify, not authority to copy.

### Explorer

Use one Explorer only under the Standard uncertainty gate. It is read-only and returns:

```text
EVIDENCE
PATHS_AND_SYMBOLS
RISKS
RECOMMENDATION
```

The recommendation is non-binding. Root verifies material claims before placing them in the Task Brief.

### Implementer

One Standard Implementer owns tracked source, configuration, and tests. It may not delegate. It returns:

```text
CHANGED_FILES
IMPLEMENTATION_SUMMARY
ACCEPTANCE_TO_EVIDENCE
COMMANDS_AND_RESULTS
LIMITATIONS
```

A correction must be scoped to blocking, reproducible findings and retains the same Implementer.

### Verifier

A fresh, read-only Verifier is required only when:

- `high-risk` applies;
- a material public API or architecture decision retains risk after deterministic checks;
- a criterion cannot be sufficiently covered by deterministic evidence;
- a concrete residual risk is identified after checks.

It is not required merely because more than one file changed, a style preference exists, or generic “extra review” is desired.

The verifier returns findings, not authorization:

```text
FINDINGS
EVIDENCE
REPRODUCTION_OR_CRITERION
COMMANDS_AND_RESULTS
LIMITATIONS
```

Each blocking finding must be reproducible, contradict a criterion, violate applicable policy, or demonstrate a concrete failure path with material impact. Speculation, unsolicited refactors, and style preferences are non-blocking risks unless the request or policy makes them criteria.

## Evidence gates and terminal states

Before calculating a terminal state, Root must inspect:

1. scope and diff against the intended candidate;
2. build, type, format, lint, and focused tests applicable to the repository;
3. integration, E2E, runtime, UI, API, log, or database proof when a criterion requires it;
4. baseline failures so pre-existing failures are not attributed to the candidate;
5. required human approval for irreversible/external effects.

A check result is valid only when tied to the candidate state it evaluates. Narrated or copied results without commands, status, or observable proof are insufficient.

| State | Conditions |
|---|---|
| `VERIFIED` | Every required criterion has valid evidence; no gate failed; no unresolved blocking finding exists. |
| `VERIFIED_WITH_RISKS` | Required criteria have valid evidence; documented residual risks are non-blocking and actionable. |
| `FAILED` | A criterion, policy/scope gate, required check, or reproducible blocking finding fails. |
| `BLOCKED` | Required information, permission, tool, environment, or human approval is unavailable, so a truthful terminal decision cannot be made. |

A verifier opinion cannot turn `FAILED` or `BLOCKED` into `VERIFIED`.

## Correction and stop semantics

v1.2 permits at most one correction attempt.

1. If deterministic checks fail, a required criterion lacks evidence, or a verifier produces a blocking reproducible finding, mark the candidate `FAILED` pending correction.
2. The Standard Implementer may make one scoped correction. Direct tasks that are promoted to Standard use the Standard Implementer for that correction.
3. Re-run affected deterministic checks. Use a fresh Verifier only if the review gate still applies.
4. Stop with the calculated terminal state after the correction. Do not retry a second time.
5. Stop immediately as `BLOCKED` for missing material context, permission, tool/environment, or required human approval.

## Checkpoints and final synthesis

After each role or evidence gate, report only:

- `Completed`
- `Status`
- `Progress`
- `Next`

Do not include raw logs or hidden reasoning.

Final synthesis reports terminal state, criterion status, changed files, implementation summary, commands/results, evidence, residual risks or blockers, and limitations.
