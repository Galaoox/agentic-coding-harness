# Codex package

This package contains `codex-orchestrator` v1.3. It does not install or configure Codex.

## Contents

```text
skills/codex-orchestrator/
├── SKILL.md                 Explicit activation and conditional loader
├── agents/openai.yaml       Codex UI metadata
└── references/
    ├── index.md             Route gates and reference map
    ├── direct.md            Direct-only mechanics
    ├── standard.md          Standard roles and ownership
    ├── evidence.md          Evidence gates and terminal states
    ├── model-routing.md     Sol/Terra/Luna and effort policy
    ├── model-routing.yaml   Machine-readable effort ceiling and default roles
    ├── long-running.md      Conditional continuity modifier
    └── high-risk.md         Conditional safety modifier
```

The skill loads only the selected route, applicable modifiers/model policy, and the evidence phase. Sol uses `medium` by default and `high` as the hard ceiling.

## Requirements

- Codex with local skills and subagents.
- Git for the target project.
- Permission to run required deterministic checks.
- Actual availability of any selected model; missing required capability yields `BLOCKED`.

Prompt rules are not a sandbox. Use Codex sandboxing, a worktree, or a container when filesystem/process isolation matters.

## Install

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R packages/codex/skills/codex-orchestrator "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is unset, inspect the installed Codex documentation or use an explicit temporary profile. Restart/open a new session and invoke explicitly:

```text
$codex-orchestrator
```

## Upgrade and uninstall

Replace or remove the installed `codex-orchestrator` directory. v1.3 replaces the old monolithic `references/orchestration-contract.md` with modular references; replace the complete directory rather than overlaying files so the obsolete file is not retained.

## Validate

```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/validate_codex_package.py
uv run python scripts/validate_knowledge_base.py
uv run python scripts/report_context_budget.py
```

Behavioral cases remain in [`../../docs/evaluation/v1.2-smoke-cases.md`](../../docs/evaluation/v1.2-smoke-cases.md) until a new runtime-backed result set supersedes them.
