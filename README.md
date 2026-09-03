# Agentic Coding Harness
<!-- supported-runtimes: codex, opencode -->

A multi-runtime monorepo for bounded, evidence-driven software-development workflows with progressive context loading.

Supported adapters:

- Codex v1.3 — explicitly invoked skill; Sol `medium` by default and `high` as the hard ceiling.
- OpenCode v0.2 — project-scoped command/agent overlay, provider-neutral and validated against OpenCode 1.18.x.

## Knowledge and context

[`AGENTS.md`](AGENTS.md) is the compact map. [`docs/index.md`](docs/index.md) is the human knowledge index and [`docs/knowledge-base.yaml`](docs/knowledge-base.yaml) declares normative documents and context scenarios. Route, modifier, model, and evidence references load only when applicable.

## Workflow

Exactly two routes are supported:

| Route | Use when | Flow |
|---|---|---|
| `Direct` | Outcome, edit location, risk, and deterministic evidence are clear | Root implements → checks → terminal state |
| `Standard` | Any Direct gate is false or uncertain | Explore if gated → one Implementer → checks → gated fresh review → terminal state |

`long-running` and `high-risk` modify Standard; they are not routes. Work remains serial with one writer for coupled changes and at most one correction.

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
  packages/opencode/install/install.py \
  packages/opencode/install/verify_install.py
git diff --check
```

Static validation proves structure and declared invariants, not model behavior. Runtime evidence and limitations live under [`docs/evaluation/`](docs/evaluation/).

## Status

Experimental. Runtime capability and behavioral claims are version-specific and must be revalidated against the current candidate.

## License

Apache-2.0
