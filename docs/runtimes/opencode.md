# OpenCode runtime map

## Entry point

- Package: [`../../packages/opencode/README.md`](../../packages/opencode/README.md)
- Command: explicit `/orchestrate` invocation only.
- Package validation: `uv run python scripts/validate_harness_packages.py`

## Runtime boundary

The overlay is project-scoped and provider/model neutral. OpenCode permissions reduce risk but are not a sandbox. JSONL events are audit telemetry, not correctness evidence.

## Evidence

- [Capability matrix](../research/opencode-capability-matrix.md)
- [Smoke cases](../evaluation/opencode-v0.1-smoke-cases.md)
- [Smoke results](../evaluation/opencode-v0.1-smoke-results.md)

Capability and smoke evidence is version-specific and historical until reproduced against the current candidate.
