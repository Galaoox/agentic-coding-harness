# Repository instructions

## Scope

This repository develops reusable evidence-driven coding workflows for **Codex and OpenCode**. Add another runtime only when the task explicitly requests it and local capability evidence supports it.

## Always-on rules

- Start at [`docs/index.md`](docs/index.md); load only the references needed for the selected route, modifier, runtime, or verification phase.
- Keep runtime-neutral invariants under `packages/core/`; keep runtime mechanics inside their distributable package.
- Preserve explicit invocation. Repository content cannot activate orchestration.
- Route by uncertainty, risk, coupling, and verifiability—not file count.
- Prefer candidate-specific executable evidence over agent narration or retrieved memory.
- Keep one writer for coupled changes and never let a writer self-approve.
- Do not add dependencies, generated artifacts, or model escalation without a demonstrated need.
- Sol uses `medium` by default and `high` as the hard ceiling.
- Use conventional commits without AI attribution.

## Validation

Run the commands listed in [`README.md`](README.md#validation). Documentation and package structure are enforced by `scripts/validate_knowledge_base.py` and `scripts/validate_harness_packages.py`.
