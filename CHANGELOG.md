# Changelog

All notable changes to this repository are documented here.

## Unreleased

- OpenCode adapter v0.5 targets stable OpenCode >=2.0.24,<3 using native ordered
  permissions, discoverable worker subagents and V2 command metadata. Installation
  manifests record runtime major 2. Smokes reject unsupported executables before
  model calls and use private servers and explicit model variants; V1-only flags
  are rejected. Usage reports distinguish root-session tokens from worker costs.

- OpenCode v0.4 activates when its primary agent is selected; ordinary requests
  need no command prefix. `/orchestrate` remains an optional shortcut.

- Codex v1.4 / OpenCode v0.3 specify all six shared capabilities, with model conformance reported separately.
- Windows/Linux CI, portable catalog paths, complete install inventories and Verifier shell-policy validation.
- Externally checked runtime smoke adapters, candidate snapshots, structured timeouts and measured usage.
- LF-normalized context budgets and optional observations by context layer and role.

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
