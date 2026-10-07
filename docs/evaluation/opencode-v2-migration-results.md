# OpenCode 2 migration evidence

Observed on Windows, 2026-10-06. Adapter `0.5.0` targets stable OpenCode
`>=2.0.24,<3`; the tested runtime is exactly `2.0.24`. These results apply to
the uncommitted candidate based on `e1f40cf`, not every future 2.x release.

## Adapter and registration

The package uses native ordered `permissions`, `subagent` command metadata,
`experimental.subagent_depth` and `mcp.servers`. Workers remain discoverable
subagents; the Root is a selectable primary. Installation manifests identify
runtime major 2. The overlay installer remains separate from runtime installation.

A cold `debug agents` returned an empty catalog with exit 0. The same location
in one persistent private server registered all four agents on the next catalog
query. The smoke runner now checks their actual instructions, modes and ordered
permissions, plus command registration, before invoking a model. Unknown agent
selection alone is insufficient evidence. The [plugin service describes this
activation race](https://github.com/anomalyco/opencode/blob/v2.0.24/packages/core/src/plugin/service.ts).

## Model-backed trials

All trials used `openai/gpt-6.1-sol#medium`, a 300-second model-process bound,
fresh Git fixtures and external checks. Candidate scope and immutable acceptance
verification are required in addition to reported state.

| Case | Evaluation | External acceptance | Root tools / delegations | Duration |
|---|---|---|---|---|
| Direct | PASS / functional_pass | exit 0; only calculator.py changed | 16 / 0 | 53.969 s |
| Standard | PASS / functional_pass | exit 0; only calculator.py changed | 10 / 2 | 115.109 s |
| High-risk | PASS / functional_pass | exit 0; only calculator.py changed; fresh Verifier executed acceptance | 14 / 4 | 245.704 s |

Direct had a terminal JSONL step. Standard and high-risk used the release-specific completion
source `cli_exit_after_session_wait`: v2.0.24 can omit the terminal step while
reconciling final text after waiting for idle. Its trace remains explicitly
incomplete and its observed usage partial. The fallback requires exit 0, no
trace errors, a terminal state, permitted scope and passing immutable external
checks; it does not apply to other runtime versions. See the [inspected CLI
implementation](https://github.com/anomalyco/opencode/blob/v2.0.24/packages/cli/src/run/noninteractive.ts).

Root-session observed input/output/cache-read/reasoning/cache-write tokens:
Direct `19950 / 1332 / 154112 / 60 / 0`; Standard
`17790 / 1215 / 41088 / 15 / 0`; high-risk
`11402 / 1983 / 64896 / 132 / 0`. These do not include established aggregate
worker costs. Sanitized Standard session exports showed Explorer using only
read/glob tools with no changed files, and Implementer executing the patch with
only `calculator.py` in its changed-file snapshots. No speed/cost comparison or
full contract conformance is claimed.

High-risk session exports showed one continuing Implementer making the candidate,
exact rollback and reapplication patches, all confined to `calculator.py`, followed
by a fresh Verifier using read/shell tools with no changed files. Four subagent
calls represent two distinct worker sessions, not four independent writers.
The final case rejects nonstrings and custom-equality objects/string subclasses.
An earlier ordinary-equality trial returned `VERIFIED_WITH_RISKS` and failed the
strict terminal requirement; it was not promoted. Stronger external negative
assertions and an explicit plain-string boundary resolved that uncertainty.

Candidate identities for the passing trials:

| Case | Before | After |
|---|---|---|
| Direct / Standard | `7f1f7906eceabb0c305da7010da944ef5773a534e8ae061a15b0575796360fb4` | `8ac5bf211fd3860fd10b6baff4e93046851fd50db9cd1bd4a30cbf515550f44d` |
| High-risk | `b6c5c14ca823d097a80539ce05bf8c6ff3438cf56894ba4f8b4e5a5917c6c131` | `ede9afb71cf9ec99cc7e2ccb433d7a2f4192ff7cfd74ab54a42176dc45dea44a` |

Direct and Standard preceded the strengthened high-risk-only assertions; their
addition criteria were unchanged. The package's agent metadata remained the same.

Initial trials exposed evaluation issues, retained as failures rather than
silently promoted: the shared fixture contained an exhausted correction brief;
fixtures under `.codex` inherited its ancestor `AGENTS.md` and attempted an
approval-gated external RTK read. Case preparation now isolates causal history.
Standard's passing fixture is outside that ancestor and uses an explicit empty
V2 global config directory. Authentication and other home/project discovery
remain shared. High-risk preparation supplies a read-only pytest acceptance
entrypoint using the existing Verifier allowlist and repository environment,
without expanding package permissions.

Raw results, session exports and registration evidence remain outside Git under
the host's `.codex/tmp` directory. Passing outcome assertions alone does not prove
writer ownership or independent review; actor traces must also be inspected.

## Native interface

In an owned interactive terminal using runtime 2.0.24, Shift+Tab cycled Build →
Plan → Harness-Orchestrator → Build. Ctrl+X then A showed only those three primary
agents; workers did not appear as primary choices. Typing `/orchestrate` displayed
the registered optional shortcut. No model request was sent in this interface
check; interactive command execution remains unmeasured. Ordinary agent-selected
requests are covered by the model-backed CLI trials.

## This PC

The installed standalone binary is in `%LOCALAPPDATA%/Programs/OpenCode/bin`.
User PATH now prefers it; the old Bun `opencode-ai` package was removed. Existing
Codex/terminal processes retain their inherited PATH and require reopening.

Global agents and MCP configuration were translated to V2 while preserving
global instruction bytes and provider authentication. Effective MCP status showed
codebase-memory-mcp, codegraph, context7 and engram connected. Incompatible Warp,
local RTK/Engram plugin hooks, and V1 TUI extensions were disabled or archived;
the native MCP integration remains available. Native V2 `cli.json` replaces the
active TUI configuration; old TUI settings are retained for recovery.

The pre-migration backup is `.codex/backups/opencode-v1-20261006-v2-migration`
under the user's home. It includes a consistent SQLite backup, config, state,
authentication/data, Bun metadata and old launcher metadata. `restore-v1.py`
defaults to a read-only dry run; `--apply` requires OpenCode closed, reinstalls
the old Bun package, preserves V2 directories and restores the original snapshot
and PATH. Dry run and compilation passed; destructive rollback was not executed.
The backed-up Bun launcher is not a standalone runtime binary.

## Deterministic checks and limits

146 tests passed; one optional live test skipped in the ordinary suite. The
explicit V2 registration test separately passed against the installed runtime.
Package, knowledge-base and Codex validators passed; all declared context budgets
passed. Compilation and whitespace checks passed. Remote Linux CI was not run.
No custom harness TUI, commit or push was created during this migration.
