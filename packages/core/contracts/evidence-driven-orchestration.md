# Evidence-driven orchestration invariants

This contract contains runtime-neutral invariants. Runtime packages retain their own activation, agent names, permissions, and lifecycle mechanics.

## Authority

Current request and executed, candidate-specific evidence outrank policies, repository history, retrieved memory, and agent narration. Memory is a lead, not a decision; reviewer opinion cannot override failed or missing evidence.

## Routing

There are exactly two routes: `Direct` and `Standard`.

- `Direct` is allowed only when the request is unambiguous, the edit location is known after short inspection, no material decision remains, the change is low-risk and reversible, and deterministic evidence can cover every criterion.
- `Standard` is required whenever a Direct gate is false or uncertain. It has one writer for coupled changes.

`long-running` and `high-risk` are modifiers, not routes. `high-risk` requires rollback planning, relevant positive/negative checks, a fresh verifier, and human approval before irreversible or external effects.

## Evidence and stopping

Every criterion must have candidate-specific executable or inspectable evidence. A task permits at most one correction. Terminal states are `VERIFIED`, `VERIFIED_WITH_RISKS`, `FAILED`, and `BLOCKED`.

A terminal claim is `VERIFIED` only when every required criterion has valid evidence. Failed checks, a scope/policy failure, or a reproducible blocking finding yield `FAILED`. Missing material context, permission, environment, tool, or human approval yields `BLOCKED`.
