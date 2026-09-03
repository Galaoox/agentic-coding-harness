# OpenCode adapter

Version: `0.2.0`

This package adapts the evidence-driven `Direct | Standard` harness to OpenCode `1.18.x` using a project-scoped overlay. It remains provider/model neutral and does not configure MCP servers, global settings, plugins, SDK orchestration, or merge behavior.

## Install

```bash
uv run python packages/opencode/install/install.py --target /path/to/project --dry-run
uv run python packages/opencode/install/install.py --target /path/to/project
uv run python packages/opencode/install/verify_install.py --target /path/to/project
```

The installer copies known overlay files, records their hashes with the package version, is idempotent, aborts on conflicting destinations, and rejects manifest/symlink paths outside the managed overlay. It never overwrites `opencode.json` or `opencode.jsonc`.

Optional reviewed project fragment:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "subagent_depth": 1
}
```

## Run

Interactive entry: `/orchestrate <request>`.

```bash
opencode run --command orchestrate --format json '<request>'
```

The Root starts at `.opencode/references/index.md`, loads only the selected route and modifiers, and loads `evidence.md` before terminal acceptance.

## Guarantees and limitations

- Routes are Direct and Standard; `long-running` and `high-risk` are modifiers.
- Root writes only in Direct by contract. Standard has one Implementer writer.
- Explorer denies edit/bash/task. Verifier denies edit/task and has an approval-gated shell allowlist.
- Permissions are defense-in-depth, not sandboxing; shell can write when enabled.
- Candidate evidence, exit codes, diff, and approvals outrank narration.
- JSONL is telemetry, not proof of correctness.
- Engram is optional historical context; `examples/engram-mcp.jsonc` is a non-working placeholder shape.

## Upgrade and uninstall

v0.2 replaces the monolithic orchestration reference with modular references. Because installation is conflict-safe, uninstall a matching v0.1 overlay before installing v0.2, or review/remove only the obsolete managed reference after preserving local modifications.

```bash
uv run python packages/opencode/install/install.py --target /path/to/project --uninstall
```

Uninstall removes only manifest-tracked files whose hashes still match. Runtime-created package metadata, lockfiles, or `node_modules` are not installer-owned.

See [`../../docs/research/opencode-capability-matrix.md`](../../docs/research/opencode-capability-matrix.md) and [`../../docs/evaluation/opencode-v0.1-smoke-results.md`](../../docs/evaluation/opencode-v0.1-smoke-results.md) for version-specific historical evidence.
