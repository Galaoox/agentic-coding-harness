# Changelog

All notable changes to this repository are documented here.

## Unreleased

### Added

- Repository knowledge map and machine-readable catalog with authority, status, runtime, and context scenarios.
- Conditional route, modifier, model-routing, and evidence references for Codex v1.3 and OpenCode v0.2.
- Deterministic context-size reporting and knowledge-base validation.
- CI gates for tests, package structure, documentation integrity, Python compilation, and diff hygiene.

### Changed

- `AGENTS.md` is now a compact table of contents and accurately declares Codex/OpenCode support.
- Sol uses `medium` by default and `high` as the hard ceiling; Terra is the everyday Standard worker and Luna handles mechanical strongly checked work.
- Runtime contracts load Direct or Standard selectively and load `long-running`/`high-risk` only when gated.
- The OpenCode installer records the package version dynamically, verifies every modular reference, and rejects manifest or symlink paths that escape the managed overlay.

### Removed

- Monolithic always-loaded `orchestration-contract.md` files from both runtime packages.

## Previous unreleased work

- OpenCode v0.1 project-scoped overlay, installer, validator, capability matrix, and smoke runner.
- Codex v1.2 Direct/Standard routing, modifiers, evidence terminal states, and gated roles.
