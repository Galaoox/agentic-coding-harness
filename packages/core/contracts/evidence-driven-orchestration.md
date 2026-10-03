# Evidence-driven orchestration invariants

This is the canonical runtime-neutral contract. Runtime packages retain activation, agent names, tools, models, permissions, installation, and lifecycle mechanics. The current adapters do not yet implement every rule here; see the [conformance gaps](../../../docs/contracts/index.md#adapter-conformance-gaps). Updating this contract does not activate orchestration or change an installed adapter.

## Authority

Current request and executed, candidate-specific evidence outrank policies, repository history, retrieved memory, and agent narration. Memory is a lead, not a decision; reviewer opinion cannot override failed or missing evidence.

## Routing

There are exactly two routes: `Direct` and `Standard`.

- `Direct` is allowed only when the request is unambiguous, the edit location is known after short inspection, no material decision remains, the change is low-risk and reversible, and deterministic evidence can cover every criterion.
- `Standard` is required whenever a Direct gate is false or uncertain. It has one writer for coupled changes.

A bounded error alone does not force Direct escalation. Reclassify when uncertainty, risk, coupling, or insufficient verification invalidates its gates. Roles remain serial; an implementer cannot self-approve or delegate coupled writing.

`long-running` and `high-risk` are modifiers, not routes. `long-running` supports cross-session continuity on either route; unit or file counts do not activate it. `high-risk` excludes Direct and requires rollback planning, relevant positive/negative checks, a fresh verifier, and human approval before irreversible or external effects. Git checkpoints require explicit authorization.

## Planning and continuity

Ordinary planning is brief and inline. A durable execution plan is optional unless explicitly requested or needed for cross-session continuity or unresolved dependencies. There is no universal plan path or required template; use the target project's convention. When persistence is unavailable, deliver the complete plan inline and label it not persisted.

Planning-only requests stop at plan delivery. Readiness is not execution authorization. An implementation request authorizes routine accepted-scope work without a second approval to start; material scope changes, functional choices, conflicting user work, and irreversible effects still require resolution or approval.

Root alone maintains the plan, including on Standard; this planning-artifact exception does not permit implementation edits. Keep one source for objectives, acceptance IDs, dependencies, readiness, authorization, decisions, actual evidence, and the next unit. A handoff binds the plan revision and assigned unit; a missing or stale binding blocks affected work. On resume, reconcile current code and user changes before relying on old readiness or evidence. Do not silently restore an old baseline, weaken criteria, or reset defect budgets.

## Investigation and reproduction

Use bounded read-only investigation only when it resolves uncertainty. A handoff includes the question, known facts, sources, allowed tools, limits, required evidence, and stopping condition. Different runtimes may map these capabilities to different actors without changing the contract.

One exceptional independent premise check is permitted per change when a material, unproven premise has important consequences and available evidence cannot resolve it. Use a fresh read-only investigator independent of the premise's author; no debate, reviewer chains, or new correction budget. An unresolved or refuted premise blocks only dependent actions, without removing required high-risk verification.

For bugs, attempt the smallest existing-stack reproduction before affected source edits. Reproduction is recommended unless the user or project explicitly requires pre-edit RED; strict TDD is also explicit or project-required. A setup failure is not RED, and detection consumes no correction attempt. Record the mode/source, runner, working directory, actual result, and limitations. Mandatory missing RED blocks dependent edits; recommended unavailable reproduction permits only disclosed, safely justified, verifiable continuation. Rerun the reproduction and affected checks after correction. Separate required fix validation from original-incident reproduction: post-fix success cannot prove historical RED.

## Evidence integrity

Every criterion needs candidate-specific executable or inspectable evidence. Capture candidate state before and after a bounded verification batch with no intervening edits; retain each command, working directory, exit status, and result. Keep plan updates outside the batch. Unexpected mutations prevent acceptance until investigated and affected checks rerun against the final candidate. Expected outputs, plan checkboxes, readiness, telemetry, and reviewer narration are not passing evidence.

When browser behavior is required, deterministic scenarios and assertions govern acceptance. Screenshots support assertions but do not replace them. Record the target, allowed side effects, commands, results, and artifacts; do not skip scenarios or weaken tests to force a pass. Never run unattended production flows or persist credentials as evidence. Browser tools, test frameworks, and role configuration remain adapter mechanics, not shared mandates.

## Root-defect corrections

Allow at most three corrections per independent root defect. Detection and investigation are not corrections; an attempted corrective change consumes one attempt, even when ineffective. Several symptoms of the same cause share one budget. Distinct causes have separate budgets only when evidence supports their independence; uncertainty about cause identity does not authorize a fresh budget.

Keep a stable defect record with the cause or current causal hypothesis, affected criteria/actions, and attempt count. For each correction, record before evidence, hypothesis, change, after evidence, and outcome. Changing route, actor, session, label, or defect name never resets or replenishes the budget. Carry the record in the existing brief or plan, not a mandatory extra artifact.

Before each correction, record its ordinal as attempt x/3, the observed failure, causal hypothesis, and intended change. After each correction, record actual checks and outcome; if unresolved, state the failure reason or explicitly mark the cause unknown before deciding the next permitted action.

If the third correction leaves the defect unresolved, stop dependent work and record the residual failure or blocker. Unrelated work may continue only when its independence is evidenced. An unresolved required defect prevents VERIFIED and VERIFIED_WITH_RISKS; an optional, non-blocking residual risk must be explicitly identified, never relabeled to evade a required criterion.

## Evidence and stopping

Terminal states are `VERIFIED`, `VERIFIED_WITH_RISKS`, `FAILED`, and `BLOCKED`. Evaluate them against required criteria and unresolved defect records, not a task-wide retry counter.

A terminal claim is `VERIFIED` only when every required criterion has valid evidence and no required defect remains unresolved. `VERIFIED_WITH_RISKS` additionally permits only explicit non-blocking residual risks. Failed checks, a scope/policy failure, or a reproducible blocking finding yield `FAILED`. Missing material context, permission, environment, tool, or human approval yields `BLOCKED`. Stopping a defect does not prevent reporting separately evidenced independent work, but cannot make the dependent scope verified.
