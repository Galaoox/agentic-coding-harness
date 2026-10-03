# Evidence and terminal states

Attempt the smallest existing-stack bug reproduction before edits. RED/TDD is mandatory only when user/project-required; otherwise reproduction is recommended. Setup failure is not RED. Record mode/source, runner, cwd, result and limitations. Mandatory missing RED blocks edits; unavailable recommended reproduction requires disclosed, safe, verifiable continuation. Post-fix success cannot prove historical RED.

Check scope/diff, applicable build/type/lint/tests, criterion-specific runtime evidence, baseline failures and approvals. Bind commands, cwd, exit status and results to candidate state before and after a verification batch with no intervening edits. Plan updates stay outside. Unexpected mutations invalidate affected evidence until investigated and rerun.

Browser acceptance needs deterministic scenarios/assertions; screenshots support them. Record target, allowed side effects and results. Never weaken checks, run unattended production flows or persist credentials.

## Corrections

Allow up to three corrections per independent root defect. Detection/investigation do not count; attempted corrective edits count even if ineffective. Same-cause symptoms share a budget; independent causes require evidence. Unknown identity grants no new budget. Route, actor, session or label changes never reset counts.

In the existing brief/plan keep cause/hypothesis, affected criteria/actions and count. Before correction record attempt x/3, failure, hypothesis and intended change. After correction record before evidence, change, after evidence, outcome and failure reason or unknown cause.

Unresolved attempt 3 stops dependent work. Independent work needs evidence of independence. Unresolved required defects prevent both verified states.

| State | Gate |
|---|---|
| VERIFIED | Every required criterion has candidate-specific evidence; no unresolved required defect. |
| VERIFIED_WITH_RISKS | Same gates; only explicit non-blocking residual risks. |
| FAILED | Required check, scope/policy or reproducible blocking finding fails. |
| BLOCKED | Material context, tool, environment, capability or approval missing. |

Narration, memory, telemetry and review cannot override these gates. Never relabel a required defect as optional risk.
