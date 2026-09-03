# Codex runtime map

## Entry point

- Skill: [`../../packages/codex/skills/codex-orchestrator/SKILL.md`](../../packages/codex/skills/codex-orchestrator/SKILL.md)
- Activation: explicit `$codex-orchestrator` invocation only.
- Package validation: `uv run python scripts/validate_codex_package.py`

## Conditional references

The skill classifies the route first, then loads the matching route contract. Evidence, model routing, `long-running`, and `high-risk` references are loaded only in their applicable phase.

## Model policy

Sol is `medium` by default and `high` is the hard ceiling. Terra handles everyday Standard engineering, exploration, difficult bounded debugging, and normal verification. Luna handles mechanical, tightly specified work with strong deterministic checks.

## Evidence

- [Codex v1.2 smoke cases](../evaluation/v1.2-smoke-cases.md)
- [Codex v1.2 smoke results](../evaluation/v1.2-smoke-results.md)

Historical smoke output does not validate a new candidate. Re-run applicable checks.
