# Harness evolution implementation results

Recorded on 2026-10-03 against the working candidate derived from `01e95cf`.
Codex package v1.4.0 and OpenCode package v0.3.0 now specify the six shared
capabilities. Full model-backed conformance remains pending.

## Implemented scope

- Catalog identities and installation manifest keys use POSIX paths on both OSes.
  CI is configured to run the deterministic suite on Windows and Ubuntu.
- OpenCode verification requires the exact managed inventory and package hashes,
  preserves unmanaged files and rejects broader Verifier shell permissions.
- Both self-contained adapters carry causal three-correction budgets, Direct
  reclassification gates, continuity on either route, optional Root-owned plans,
  current handoffs, reproduction policy and immutable verification. Exceptional
  premise checks remain bounded; browser acceptance needs executable assertions.
- Shared bounded smoke adapters inspect external checks, untracked/deleted files,
  typed file/link identities and verification mutation. Timeouts terminate the
  owned process tree. Missing terminal state, false success and expected blockers
  have separate outcomes. Eight scenario definitions are supplied.
- Context budgets normalize checkout line endings and report package bytes,
  explicit per-role layer inputs and runtime-reported tokens separately.
- Only the authorized Gentle blocks were removed from global Codex/OpenCode
  instructions. Backups were retained; byte comparisons proved remaining bytes
  unchanged. RTK/advisor instructions and unrelated `.atl/` remain intact.

## Deterministic evidence

On Windows, `uv sync --frozen`, `uv run pytest -q`, the knowledge-base, combined
harness and Codex validators, the context report, Python compilation and
`git diff --check` pass. The suite reports **105 passed, 1 skipped**; the skip is
the optional externally provisioned OpenCode discovery fixture. Linux CI is
configured but has not been executed locally or remotely in this task.

Regression coverage includes actual failing/passing fixture assertions, both
runtime adapters, unsafe manifest inventories/permissions, unauthorized changes,
missing/labelled terminal states, failed checks, verification mutation followed
by restoration, inaccessible evidence, Windows launchers, malformed cases and
termination of an innocent child process after timeout.

A read-only peer found launcher portability, terminal parsing, mutation batching,
child cleanup and file/link identity defects during the implementation. These
were corrected and covered by regressions. Peer observations supplement checks;
they do not substitute for behavioral evidence or approve delivery.

## Package context

LF-normalized UTF-8 bytes; global rules, hidden prompts and runtime overhead are
excluded. All declared scenarios meet their reviewed budgets.

| Scenario | Codex bytes / limit | OpenCode bytes / limit |
|---|---:|---:|
| Direct | 6,235 / 6,500 | 5,253 / 5,500 |
| Direct + continuity | 6,936 / 7,500 | 5,954 / 6,500 |
| Standard | 8,124 / 8,500 | 5,784 / 6,000 |
| Standard + high-risk | 8,869 / 9,500 | 6,329 / 6,800 |
| Standard + continuity | 8,825 / 9,500 | 6,485 / 7,000 |

Repository bootstrap is 1,310 / 1,600 bytes. Against the prior recorded progressive
package measurements, Codex Direct is about 1.8% smaller and Standard 1.5% larger;
OpenCode Direct/Standard grow about 7.3%/16.7% because formerly absent safeguards
are now specified. Reviewed OpenCode caps were increased for those guarantees.
This is not a claim of universal token savings.

## Live runtime evidence

Direct trials use disposable fixtures, explicit invocation, Sol `medium`,
existing provider authentication and externally executed outcome assertions.
Raw traces remain outside Git. `--clean-config` is partial isolation: remaining
global rules and MCP registrations can still affect discovery and context.

| Trial | Runtime / model | Outcome | Observation |
|---|---|---|---|
| Codex final Direct, 120-second process limit | CLI 0.160.0 / gpt-6.1-sol | BLOCKED | Runtime reported read-only sandbox; command execution rejected by policy; no file changes |
| OpenCode first Direct, 120-second limit | 1.18.34 / openai/gpt-6.1-sol | BLOCKED: timeout | One scoped calculator edit; no completed terminal response |
| OpenCode cold-discovery Direct, 300-second limit | 1.18.34 / openai/gpt-6.1-sol | FAIL: false_green | Product assertions passed but 3,671 paths changed, including runtime-generated installation files; reported VERIFIED was rejected |
| OpenCode prepared-discovery Direct, 300-second limit | 1.18.34 / openai/gpt-6.1-sol | PASS: functional_pass | Only calculator.py changed; external outcome check passed; verification preserved the candidate |

The final Codex trial reports 70,443 input tokens, 349 output tokens, 59,264 cached
input tokens and 26.109 seconds. The cold OpenCode trial reports 21,765 input,
1,871 output, 192,896 cached-read tokens and 160.891 seconds. Provider fields have
different semantics and must not be added together or treated as comparable
total context. These runs are not an A/B comparison.

The prepared OpenCode trial reports 26,841 input tokens, 3,267 output tokens,
331,648 cached-read tokens, 22 tool calls, zero task delegations and 262.687
seconds. Its pass establishes this Direct outcome and scope, not Standard role
ownership or full cross-runtime parity. Remaining global context and provider
behavior are not isolated enough to attribute those costs to package bytes.

Prepared-trial candidate identities: before
`2321708b80eff5c99fbdbd8563dc2b7b1f9cf531bbc5a60628ae83a961e9be7f`;
after and during external verification
`2f49774f8f8484d43cf0fc8dd96ab229b23d33723359e8082d9fdec5a536ba61`.
The trace includes optional CodeGraph and Engram calls; corrections and human
interventions remain unmeasured. Source traces are `opencode-discovered-direct.json`
and `codex-final-direct.json` in the external evaluation directory.

## Remaining release evidence

Resolve the legitimate Codex environment restriction without weakening security,
run the full [case corpus](harness-smoke-guide.md) on matched profiles and inspect
actor traces for ownership, current handoffs, fresh review and correction limits.
A passing arithmetic outcome alone cannot prove the six capabilities. Do not
publish full parity, cost superiority or a Standard role change from these runs.
The implementation plan remains active for this behavioral evidence, remote CI
execution and the deferred delegation experiment.
