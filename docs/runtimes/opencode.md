# OpenCode runtime map

## Entry point

- Package: [`../../packages/opencode/README.md`](../../packages/opencode/README.md)
- Runtime target: stable OpenCode >=2.0.24,<3; adapter v0.5.0.
- Interactive entry: select `harness-orchestrator` with Shift+Tab or the agent selector,
  then send ordinary requests while selected.
- CLI entry: `opencode run --standalone --agent harness-orchestrator --model PROVIDER/MODEL#medium '<request>'`.
- Optional shortcut: `/orchestrate <request>`.
- Package validation: `uv run python scripts/validate_harness_packages.py`

## Runtime boundary

The overlay is project-scoped and provider/model neutral. OpenCode permissions reduce risk but are not a sandbox. JSONL events are audit telemetry, not correctness evidence.

## Evidence

- [OpenCode 2 migration results](../evaluation/opencode-v2-migration-results.md)

- [Current bounded smoke guide](../evaluation/harness-smoke-guide.md)

- [Capability matrix](../research/opencode-capability-matrix.md)
- [Smoke cases](../evaluation/opencode-v0.1-smoke-cases.md)
- [Smoke results](../evaluation/opencode-v0.1-smoke-results.md)

Capability and smoke evidence is version-specific and historical until reproduced against the current candidate.
