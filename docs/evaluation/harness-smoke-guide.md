# Verify outcomes with bounded runtime cases

Use disposable project fixtures and external assertions. A finished runtime
event or a `VERIFIED` response alone can never pass a functional case.

## Quick path

1. Copy `tests/fixtures/harness-smoke/project` to a disposable directory, initialize
   Git there, and install the candidate adapter. Codex accepts project skills at
   `.agents/skills`; OpenCode uses the project overlay installer.
   `scripts/prepare_smoke_fixture.py --runtime codex|opencode --case CASE_ID --target NEW_DIRECTORY`
   automates this and refuses an existing target. Select the case during preparation:
   only `causal-continuity` retains the exhausted correction brief. Omitting `--case`
   preserves the legacy shared fixture and can block unrelated implementation trials.
2. Prepare runtime discovery before taking the baseline, keeping personal plugins
   and unrelated global instructions out of the evaluation profile. Share only
   the authentication required by the chosen provider; never copy auth to fixtures.
   OpenCode 2 activates plugins asynchronously: a successful cold `debug agents`
   can return an empty catalog. The runner owns one loopback server and polls
   that server/location for matching agent instructions, modes, ordered permissions,
   and the registered command before any model call. Failure blocks evaluation.
   Discovery can create runtime files; capture output outside the candidate and Git.
   Do not ignore these paths or widen allowed edits to hide a cold-start mutation.
3. Run one case, supplying the model and bounded time explicitly:

```bash
uv run python scripts/run_codex_smoke.py --fixture /path/to/fixture --case tests/fixtures/harness-smoke/cases/direct.json --model YOUR_SOL_MODEL --effort medium --timeout 120
uv run python scripts/run_opencode_smoke.py --fixture /path/to/fixture --case tests/fixtures/harness-smoke/cases/direct.json --model YOUR_PROVIDER_MODEL --effort medium --timeout 120
```

Use a fresh fixture for each trial. A case is trusted evaluation configuration:
its `checks` execute argv arrays without shell interpolation. Allowed changes use
relative POSIX patterns. Required outcome assertions belong in checks outside the
agent's control; maintainers must review those assertions along with the case.

OpenCode adapter v0.5 requires stable runtime >=2.0.24,<3 before any model call.
It selects `--agent harness-orchestrator` and sends an ordinary request without
`/orchestrate`. V2 `run` cannot dispatch commands: `--entrypoint command` is
rejected; test the optional shortcut interactively. Results record the entry
point separately; CLI selection does not prove terminal keyboard navigation.

`--clean-config` uses Codex's `--ignore-user-config`. OpenCode V2 rejects this flag
because it has no `--pure`; use a separately prepared evaluation configuration.
`--config-dir EXISTING_DIRECTORY` sets native `OPENCODE_CONFIG_DIR` for the owned
server and CLI, replacing the usual global config directory. Provider authentication
and other home/project discovery remain shared; this is partial isolation.
Its runner owns a bounded private `serve` process and connects using `run --server`;
this does not isolate global rules, plugins or MCP registrations. Authentication stays in its existing store.
Record remaining configuration layers. Supply an explicit OpenCode provider/model;
the runner appends `#medium` or `#high`, rejecting conflicting supplied variants.

The runners preserve `--fixture` and `--message`. Without `--case`, execution is
diagnostic only (exit 2), never functional success. Each prompt requests a final
`HARNESS_STATE=...` marker. State is reported separately from evaluation PASS/FAIL;
an expected blocker may pass a blocking scenario but is not `functional_pass`.

## Cases and limits

The supplied corpus covers Direct, Standard, high-risk, planning-only, unavailable
approval, causal-budget continuity, browser prerequisites and resumed user changes.
External checks establish outcomes and scope; inspecting actor/tool traces is
still required to establish role ownership, fresh review and workflow compliance.
Passing a calculator outcome does not prove all six contract capabilities.

For high-risk, case preparation includes a read-only pytest wrapper around the
same external acceptance script. Run from the repository's `uv run` environment;
the Verifier can use its existing `uv run pytest *` allowlist without expanding
permissions. The wrapper and acceptance script remain outside allowed changes.
The private server supplies `PYTHONDONTWRITEBYTECODE=1` to avoid bytecode artifacts.
Authorization assertions include custom-equality objects/string subclasses;
ordinary equality alone does not establish the stated plain-string boundary.
Place evaluation fixtures outside directories with unrelated ancestor `AGENTS.md`:
changing the global config directory does not disable parent-project discovery.

Process timeout defaults to 120 seconds and is limited to 600; on timeout the
owned process tree is terminated before snapshotting. Checks have the same
per-process bound and stop after an error or mutation. One invocation is one
trial, with no automatic retries. Raw JSON output belongs outside Git and may
contain prompts/paths: do not capture credentials or publish unredacted traces.

PR CI runs deterministic smoke regressions without models. Run live cases manually
or before behavior publication. Missing runtime/auth/model/required approval is
a blocker, not proof of a behavioral defect. Record candidate fixture hash,
runtime/version, model/effort, commands, exits, scope, observations and limitations.

## Historical OpenCode v0.4 agent-entry evidence

On 2026-10-06, the candidate v0.4 overlay passed the Direct case on Windows with
OpenCode 1.18.34, `openai/gpt-6.1-sol`, effort `medium`, `--clean-config` and a
300-second limit. Discovery was prepared before the baseline. The runner selected
`--agent harness-orchestrator`; the request contained no `/orchestrate` prefix.
The runtime discovered that agent as enabled and `primary`.

The evaluator returned `PASS / functional_pass`: only `calculator.py` changed,
`python check_outcome.py direct` exited 0, and external verification preserved
the candidate. Candidate identity changed from
`8acc670f6b2a3b720a4965a5edfc4444a1ae1d8d54e03815441a5695c9be3c00` to
`02513c4cf0519911c89d2d725585b59cdce4da64223d5c48dfda6dc99fa88513`.
Raw evidence is retained outside Git as `opencode-mode-result-20261006.json`.

This establishes one Direct outcome through agent selection. It does not prove
Tab navigation, interactive switching, Standard ownership or full conformance;
global rules/MCP registrations remained partially shared. Deterministic checks
also passed: 107 tests, one optional discovery fixture skipped, package/catalog
validation and all declared context budgets.

## Cost and context

Smoke results expose duration, observed tool/delegation events and runtime token
usage. Unobservable corrections, interventions or delegation counts remain null.
Usage semantics differ by provider; compare matched runtime/model/task settings.

V2 reports input, output, reasoning, cache-read and cache-write tokens separately,
with `usage_scope: root_session`. The CLI stream filters root-session events;
these counters do not establish combined worker costs. Missing fields stay null.

The inspected runtime 2.0.24 can reconcile final text after `session.wait()` while
omitting the terminal `step_finish`. Only that exact release permits the completion
source `cli_exit_after_session_wait`, requiring exit 0, no trace errors, a terminal
state, passing external checks, permitted scope and immutable verification.
`trace_complete` remains false and `usage_complete` is false; no missing tokens
are inferred. Other versions retain the terminal-event requirement.

`report_context_budget.py` reports LF-normalized package bytes plus observed raw
bytes. Optional `--layers layers.json` accepts an array of
`{role, layer, files}` records, resolving relative files against that JSON file.
Optional `--run-result result.json` adds measured usage. Roles remain separate;
these measurements do not reconstruct hidden system prompts or infer tokens.

## Delegation experiment

After evidence is reliable, compare the existing Standard baseline with a
single-executor experimental profile using the same model, effort, task, checks,
environment and three repetitions per variant. Reset fixtures between trials.
Keep one writer and mandatory independent high-risk review in both variants.
Report success, tokens, duration, calls, corrections and human interventions with
unavailable measurements disclosed. Adopt no role change from lower cost alone;
the experiment does not change the shipped Standard ownership policy.
