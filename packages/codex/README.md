# Codex package

This package contains the Codex-specific `codex-orchestrator` skill. It is not an OpenCode adapter and it does not install or configure Codex itself.

## Contents

```text
skills/codex-orchestrator/
  SKILL.md                                Activation and operational summary
  agents/openai.yaml                      Codex UI metadata
  references/orchestration-contract.md    Normative routing and evidence contract
```

## Requirements

- A Codex installation that supports local skills and subagents.
- A Git repository for the task being orchestrated.
- Permission to run the repository's required deterministic checks.

The skill's rules guide an agent; they are not a sandbox. Use Codex sandboxing, a worktree, or a container when filesystem/process isolation matters.

## Install for a local Codex profile

Copy the skill directory into the skill location configured by your Codex installation. The commonly used layout is:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R packages/codex/skills/codex-orchestrator "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is unset, consult the installed Codex documentation or run the smoke setup with an explicit temporary `CODEX_HOME`; do not assume a user-specific home path in repository files.

Restart or open a new Codex session after installation so it discovers the skill. Invoke it explicitly:

```text
$codex-orchestrator
```

It intentionally does not activate implicitly.

## Upgrade and uninstall

To upgrade, replace the installed `codex-orchestrator` directory with the desired repository version and restart the Codex session. To uninstall, remove that installed directory. No installer or automatic migration exists in v1.2.

## Validate before installation

From the repository root:

```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/validate_codex_package.py
```

For behavioral validation, run the cases in `../../docs/evaluation/v1.2-smoke-cases.md` against a temporary Codex profile and record only real results in the matching smoke-results file.
