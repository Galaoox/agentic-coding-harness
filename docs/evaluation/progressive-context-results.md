# Progressive context evaluation

## Candidate

Measured on the progressive-context branch against baseline commit `91cd3c27669256d033abdfa88fb56a03ca6df9bd`. Values are deterministic UTF-8/file statistics, not exact model-token counts.

## Baseline

| Runtime | Always-loaded files | Bytes | Lines | Words |
|---|---:|---:|---:|---:|
| Codex | 2 | 12,282 | 250 | 1,710 |
| OpenCode | 2 | 3,710 | 41 | 493 |

Codex baseline is `SKILL.md` plus the monolithic contract. OpenCode baseline is the Root agent plus its monolithic contract.

## Progressive scenarios

| Scenario | Files | Bytes | Lines | Words | Change from matching baseline |
|---|---:|---:|---:|---:|---:|
| Repository bootstrap | 1 | 1,310 | 22 | 165 | n/a |
| Codex Direct | 4 | 6,347 | 102 | 815 | -48.3% bytes |
| Codex Standard | 5 | 8,004 | 124 | 1,047 | -34.8% bytes |
| Codex Standard + high-risk | 6 | 8,749 | 139 | 1,143 | -28.8% bytes |
| Codex Standard + long-running | 6 | 8,690 | 137 | 1,148 | -29.2% bytes |
| OpenCode Direct | 4 | 4,896 | 75 | 636 | +32.0% bytes |
| OpenCode Standard | 4 | 4,957 | 78 | 645 | +33.6% bytes |
| OpenCode Standard + high-risk | 5 | 5,502 | 85 | 705 | +48.3% bytes |
| OpenCode Standard + long-running | 5 | 5,465 | 85 | 719 | +47.3% bytes |

OpenCode grows relative to its underspecified baseline because the modular package restores required Task Brief/authority semantics and loads explicit modifier safeguards. The optimization target is irrelevant context, not minimum bytes at the expense of required controls. Every scenario is below its reviewed `max_bytes` threshold in `docs/knowledge-base.yaml`.

## Validation status

Candidate validation on 2026-09-03:

- `uv run pytest -q` → `62 passed`.
- Knowledge-base, combined-harness, and Codex validators → passed.
- Python compilation and `git diff --check` → passed.
- OpenCode `1.18.27` install dry-run, install, manifest verification, `opencode debug config` discovery, and hash-constrained uninstall → passed in a disposable temporary fixture.
- Fixture discovery test → `1 passed`.
- Codex behavioral smoke → `BLOCKED` because no local `codex` executable is installed.
- OpenCode model-backed smoke → `BLOCKED` because `opencode auth list` reports `0 credentials`.

Static package, catalog, link, context-map, and discovery evidence do not prove semantic model behavior. Historical behavioral evidence remains version-specific and is not promoted to this candidate.
