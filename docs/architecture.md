# Architecture
<!-- supported-runtimes: codex, opencode -->

Codex v1.4 and OpenCode v0.3 are self-contained adapters for the
[shared evidence-driven contract](../packages/core/contracts/evidence-driven-orchestration.md).
`AGENTS.md` is the compact entry; [the index](index.md) and
[catalog](knowledge-base.yaml) own knowledge authority and conditional context.

## Runtime boundaries

Core owns routing, planning, evidence, one writer, causal correction budgets and
terminal states. Adapters own invocation, tools, models, permissions and
installation. Both specify the six shared capability groups; the
[conformance matrix](contracts/index.md#adapter-conformance) distinguishes
specification from observed model behavior.

Direct: Root implements and verifies while every gate holds. A bounded error
alone does not escalate. Standard: gated exploration, one persistent Implementer,
deterministic checks and gated fresh review. Root maintains the plan on either
route; high-risk excludes Direct; continuity may modify either route.

Codex activates only through explicit skill invocation and retains Sol medium
with high ceiling. OpenCode activates only through `/orchestrate` and remains
provider-neutral. Its permissions are defense-in-depth: shell can write, and a
Standard Root's non-writing role is contractual. Neither prompts nor static
permission checks constitute a sandbox.

## Evidence and evaluation

Current request and candidate-specific executable evidence outrank repository
documentation, decisions, Git/issue history, retrieved memory and agent opinion.
Outcome checks never derive success from a completed event or narrated state.
The shared smoke evaluator records candidate hashes, per-command snapshots,
results, runtime/version, scope changes and usage. Runtime adapters parse their
own telemetry; unsupported metrics are unavailable rather than invented.

PR CI runs deterministic tests and validators on Windows/Linux. Model-backed
cases run manually or before behavior publication, in disposable fixtures with
explicit time budgets. Historical results remain version-specific.

Package context budgets use normalized LF bytes; observed global layers and
delegated roles are measured separately. Global memory, search and review tools
remain optional. No runtime or new dependency is added by this evolution.
