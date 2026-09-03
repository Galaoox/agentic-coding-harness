# OpenCode adapter

Version: `0.1.0`

This package adapts the evidence-driven `Direct | Standard` harness to OpenCode `1.18.x` using a project-scoped overlay. It does not configure providers, models, MCP servers, global OpenCode configuration, plugins, SDK orchestration, or automatic merge behavior.

## Install

```bash
uv run python packages/opencode/install/install.py --target /path/to/project --dry-run
uv run python packages/opencode/install/install.py --target /path/to/project
uv run python packages/opencode/install/verify_install.py --target /path/to/project
```

The installer copies only its known overlay files to `/path/to/project/.opencode/`, records a digest manifest, is idempotent, and aborts on a different destination file. It never overwrites an existing `opencode.json` or `opencode.jsonc`.

Use this optional project config fragment only after review:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "subagent_depth": 1
}
```

## Run

Normal interactive entry: `/orchestrate <request>`.

For automation after provider/model configuration:

```bash
opencode run --command orchestrate --format json '<request>'
```

`opencode run --agent harness-orchestrator` is useful only for isolated agent diagnostics; it does not validate command wiring.

## Guarantees and limitations

- Exactly two routes: Direct and Standard. `long-running` and `high-risk` are modifiers.
- Root can write only in Direct by process contract. Standard has one Implementer writer.
- Explorer denies edit, bash, and task. Verifier denies edit/task and has an approval-gated shell allowlist.
- OpenCode permissions are defense-in-depth, not sandboxing: static permissions cannot change by route, and shell may write if enabled.
- Evidence gates, exit codes, candidate diff and required approvals override agent/reviewer narration.
- Engram is optional and subordinate to current code/tests; see `examples/engram-mcp.jsonc` for a non-working placeholder shape that must be replaced with a verified project-specific server configuration.

## Uninstall / rollback

```bash
uv run python packages/opencode/install/install.py --target /path/to/project --uninstall
```

Uninstall removes only manifest-tracked files whose digests still match; it preserves modified and unrelated files. OpenCode itself may create `.opencode/package.json`, lockfiles or `node_modules`; these are not installer-owned and are left for project review/removal.

See `docs/research/opencode-capability-matrix.md` for version-specific evidence and `docs/evaluation/opencode-v0.1-smoke-results.md` for behavioral results.
