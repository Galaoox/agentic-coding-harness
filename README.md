# Agentic Coding Harness
<!-- supported-runtimes: codex, opencode -->

A multi-runtime monorepo for bounded, evidence-driven software-development workflows with progressive context loading.

Supported adapters:

- Codex v1.4 — explicitly invoked skill; Sol `medium` by default and `high` as the hard ceiling.
- OpenCode v0.3 — project-scoped command/agent overlay, provider-neutral, targeting OpenCode 1.18.x.

## Knowledge and context

[`AGENTS.md`](AGENTS.md) is the compact map. [`docs/index.md`](docs/index.md) is the human knowledge index and [`docs/knowledge-base.yaml`](docs/knowledge-base.yaml) declares normative documents and context scenarios. Route, modifier, model, and evidence references load only when applicable.

## Workflow

Exactly two routes are supported:

| Route | Use when | Flow |
|---|---|---|
| `Direct` | Outcome, edit location, risk, and deterministic evidence are clear | Root implements → checks → terminal state |
| `Standard` | Any Direct gate is false or uncertain | Explore if gated → one Implementer → checks → gated fresh review → terminal state |

The [canonical shared contract](packages/core/contracts/evidence-driven-orchestration.md) keeps one writer and permits three corrections per independent root defect, excluding detection. Budgets survive route, actor, session, and name changes; an unresolved required defect after the third correction stops dependent work and prevents verified delivery. A bounded error alone does not escalate Direct when its gates still hold.

Both adapters specify cross-session continuity on either route, authorized checkpoints and three corrections per independent root defect. High-risk excludes Direct. Static conformance and runtime evidence remain distinct: see the [conformance matrix](docs/contracts/index.md#adapter-conformance).

## Model policy for Codex

| Work | Model | Initial effort |
|---|---|---|
| Root planning and orchestration | Sol | `medium` |
| Material architecture, security, or high-risk review | Sol | `high` maximum |
| Mechanical, strongly checked implementation | Luna | `medium` or `high` |
| Everyday Standard implementation/exploration | Terra | `medium` |
| Difficult bounded debugging or normal verification | Terra | `high` |

OpenCode does not pin a provider or model.

## Evidence authority

Candidate-specific executable evidence outranks agent/reviewer narration, repository history, and retrieved memory. Terminal states are `VERIFIED`, `VERIFIED_WITH_RISKS`, `FAILED`, and `BLOCKED`.

## Repository layout

```text
AGENTS.md                         Compact always-loaded map
docs/index.md                    Repository knowledge map
docs/knowledge-base.yaml         Document and context-scenario catalog
packages/core/                   Shared invariants
packages/codex/                  Codex skill and conditional references
packages/opencode/               OpenCode overlay, installer, and verifier
scripts/                         Validators, context report, smoke tooling
tests/                           Static, installation, and runtime tests
```

## Validation

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/validate_knowledge_base.py
uv run python scripts/validate_harness_packages.py
uv run python scripts/validate_codex_package.py
uv run python scripts/report_context_budget.py
uv run python -m py_compile \
  scripts/validate_knowledge_base.py \
  scripts/validate_harness_packages.py \
  scripts/validate_codex_package.py \
  scripts/report_context_budget.py \
  scripts/run_opencode_smoke.py \
  scripts/run_codex_smoke.py \
  scripts/smoke_evidence.py \
  scripts/prepare_smoke_fixture.py \
  packages/opencode/install/install.py \
  packages/opencode/install/verify_install.py
git diff --check
```

Static validation proves structure and declared invariants, not model behavior. Runtime evidence and limitations live under [`docs/evaluation/`](docs/evaluation/).

Run [bounded model smokes](docs/evaluation/harness-smoke-guide.md) manually or before a behavior release. Each run uses external case checks; ordinary PR validation uses deterministic tests on Windows and Linux. Context reporting separates LF-normalized package budgets, observed role/layer inputs and runtime tokens. Global memory/search/review tools are optional integrations, not package dependencies.

## Status

Experimental. Runtime capability and behavioral claims are version-specific and must be revalidated against the current candidate.

## License

Apache-2.0
