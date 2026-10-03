# Verify outcomes with bounded runtime cases

Use disposable project fixtures and external assertions. A finished runtime
event or a `VERIFIED` response alone can never pass a functional case.

## Quick path

1. Copy `tests/fixtures/harness-smoke/project` to a disposable directory, initialize
   Git there, and install the candidate adapter. Codex accepts project skills at
   `.agents/skills`; OpenCode uses the project overlay installer.
   `scripts/prepare_smoke_fixture.py --runtime codex|opencode --target NEW_DIRECTORY`
   automates this and refuses an existing target.
2. Prepare runtime discovery before taking the baseline, keeping personal plugins
   and unrelated global instructions out of the evaluation profile. Share only
   the authentication required by the chosen provider; never copy auth to fixtures.
   For OpenCode, run `opencode debug config` in that fixture and check its exit
   before the trial. It can create dependency/metadata files even when the later
   run uses `--pure`; capture discovery output outside the candidate and Git.
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

`--clean-config` uses Codex's `--ignore-user-config` or OpenCode's `--pure`.
Authentication stays in its existing provider store. This does not isolate every
global rule or organizational setting; record remaining configuration layers.

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

Process timeout defaults to 120 seconds and is limited to 600; on timeout the
owned process tree is terminated before snapshotting. Checks have the same
per-process bound and stop after an error or mutation. One invocation is one
trial, with no automatic retries. Raw JSON output belongs outside Git and may
contain prompts/paths: do not capture credentials or publish unredacted traces.

PR CI runs deterministic smoke regressions without models. Run live cases manually
or before behavior publication. Missing runtime/auth/model/required approval is
a blocker, not proof of a behavioral defect. Record candidate fixture hash,
runtime/version, model/effort, commands, exits, scope, observations and limitations.

## Cost and context

Smoke results expose duration, observed tool/delegation events and runtime token
usage. Unobservable corrections, interventions or delegation counts remain null.
Usage semantics differ by provider; compare matched runtime/model/task settings.

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
