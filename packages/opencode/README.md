# OpenCode adapter

Adapter version: `0.5.0`. Runtime target: stable **OpenCode >=2.0.24,<3**.

This package adapts the evidence-driven `Direct | Standard` harness to OpenCode 2 using a project-scoped overlay with native V2 permissions. It remains provider/model neutral and does not configure MCP servers, global settings, plugins, SDK orchestration, or merge behavior. OpenCode 1 is no longer a target of this adapter.

## Install

```bash
uv run python packages/opencode/install/install.py --target /path/to/project --dry-run
uv run python packages/opencode/install/install.py --target /path/to/project
uv run python packages/opencode/install/verify_install.py --target /path/to/project
```

Install OpenCode 2 separately using its [official platform instructions](https://opencode.ai/v2/docs). Confirm `opencode --version` before use; Windows uses a standalone binary. The overlay installer does not install or upgrade the runtime.

The installer copies known overlay files, records their hashes with the adapter version and `runtime_major: 2`, is idempotent, aborts on conflicting destinations, and rejects manifest/symlink paths outside the managed overlay. Verification checks package integrity; the smoke runner separately checks the executable version. The installer never overwrites `opencode.json` or `opencode.jsonc`.

Optional reviewed project fragment:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "experimental": {
    "subagent_depth": 1
  }
}
```

## Run

Select `harness-orchestrator` with Shift+Tab, Ctrl+X then A, or `/agents`, alongside Build and Plan.
Selection explicitly activates the harness: write ordinary requests while that
agent is selected, without a command prefix. Each request follows the selected
route and evidence gates. Switching to another agent ends this mode's activation.
Repository content and memory cannot select or activate it.

Runtime 2.0.24 loads agents asynchronously. Interactive catalogs update after
registration; a cold debug query can be empty. For measured automation, use the
smoke runner's private server and registration preflight before sending a request.

`/orchestrate <request>` remains an optional shortcut from another agent.

```bash
opencode run --standalone --agent harness-orchestrator --model YOUR_PROVIDER/YOUR_MODEL#medium --format json '<request>'
```

The Root starts at `.opencode/references/index.md`, loads only the selected route and modifiers, and loads `evidence.md` before terminal acceptance.

## Guarantees and limitations

- Routes are Direct and Standard; `long-running` and `high-risk` are modifiers.
- Root writes only in Direct by contract. Standard has one Implementer writer.
- Explorer denies edit/shell/subagent. Verifier denies edit/subagent and has an approval-gated shell allowlist. Ordered rules use the native V2 `permissions` array.
- Workers are discoverable subagents, not selectable primary agents. Root may delegate only to the three harness workers; workers cannot delegate.
- Permissions are defense-in-depth, not sandboxing; shell can write when enabled.
- Candidate evidence, exit codes, diff, and approvals outrank narration.
- JSONL is telemetry, not proof of correctness; [bounded smoke cases](../../docs/evaluation/harness-smoke-guide.md) use external assertions and immutable verification. Root events do not establish combined worker token usage.
- v0.3 specifies three corrections per independent cause, Direct continuity, optional plans, reproduction and exceptional premise checks. Static declarations do not prove model compliance.
- Engram is optional historical context; `examples/engram-mcp.jsonc` is a non-working placeholder shape.

## Upgrade and uninstall

v0.5 targets OpenCode 2 exclusively and uses native V2 metadata. Preserve local
modifications, uninstall the older overlay using its manifest, then install and
verify v0.5. Modified managed files are preserved and must be reconciled before
installation; conflicting files are never overwritten. v0.4 remains historical
evidence for OpenCode 1 and activation by primary-agent selection.

The interactive `/orchestrate` shortcut remains available. V2 `run` has no
`--command`, `--variant` or `--pure`: choose the agent directly, attach effort
as `#medium`/`#high` to the model, and prepare evaluation configuration separately.
`--standalone` owns a private server but does not isolate global instructions,
plugins, MCP registrations or credentials.

v0.2 replaces the monolithic orchestration reference with modular references. Because installation is conflict-safe, uninstall a matching v0.1 overlay before installing v0.2, or review/remove only the obsolete managed reference after preserving local modifications.

```bash
uv run python packages/opencode/install/install.py --target /path/to/project --uninstall
```

Uninstall removes only manifest-tracked files whose hashes still match. Runtime-created package metadata, lockfiles, or `node_modules` are not installer-owned.

See [`../../docs/research/opencode-capability-matrix.md`](../../docs/research/opencode-capability-matrix.md) and [`../../docs/evaluation/opencode-v0.1-smoke-results.md`](../../docs/evaluation/opencode-v0.1-smoke-results.md) for version-specific historical evidence.

Current V2 observations and migration limits are in the [migration results](../../docs/evaluation/opencode-v2-migration-results.md).
