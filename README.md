# Agentic Coding Harness

A Codex-first monorepo for bounded, evidence-driven software-development workflows.

Codex is the only supported runtime in the current milestone. OpenCode and other runtimes are future work and are not implemented here.

## v1.2 workflow

`codex-orchestrator` has two routes:

| Route | Use when | Flow |
|---|---|---|
| `Direct` | The outcome, edit location, risk and deterministic evidence are all clear | Root implements → checks → terminal state |
| `Standard` | Any Direct gate is uncertain or false | Explore only if needed → one Implementer → checks → gated fresh review → terminal state |

Two modifiers apply only to Standard:

- `long-running`: independently verified units, checkpoints, and concise handoffs.
- `high-risk`: baseline, rollback, relevant negative checks, fresh review, and human approval before irreversible/external effects.

The workflow remains serial in v1.2. It does not fan out writers or reviewers.

## Principles

- Route work by uncertainty, risk, coupling, and verifiability—not file count.
- Keep one implementation owner for coupled Standard changes.
- Prefer executable evidence over agent narration.
- Run review only for explicit residual-risk gates; reviewer output is findings, not terminal authority.
- Use Engram to recover the past, never to decide the present.
- Keep required rules and authoritative decisions in versioned repository files.

## Terminal states

| State | Meaning |
|---|---|
| `VERIFIED` | Every required criterion has valid evidence and no gate failed. |
| `VERIFIED_WITH_RISKS` | Criteria have valid evidence; residual risks are documented and non-blocking. |
| `FAILED` | A criterion, required check, policy/scope gate, or reproducible blocking finding failed. |
| `BLOCKED` | Required context, permission, tool, environment, or approval is unavailable. |

A textual reviewer `PASS` cannot override failed checks, missing evidence, or a blocked approval.

## Repository layout

```text
packages/
  core/                         Shared principles, including memory authority
  codex/
    README.md                   Codex installation and package boundaries
    skills/codex-orchestrator/  Explicitly invoked orchestration skill
docs/
  architecture.md               Boundaries and extension strategy
  baselines/                    Versioned workflow comparisons
  evaluation/                   Smoke-case specs and real execution records
```

## Validation

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/validate_codex_package.py
```

The static validator checks package structure and consistency. It does not prove LLM behavior; see `docs/evaluation/v1.2-smoke-cases.md` for real Codex scenarios.

## Status

Experimental. v1.2 is a scoped evolution of the v1.1 baseline, not a complete agent framework.

## License

Apache-2.0
