# Changelog

All notable changes to this repository are documented here.

## Unreleased

### Added

- Scoped v1.2 Codex routing with `Direct` and `Standard` routes.
- `long-running` and `high-risk` modifiers for Standard work.
- Criterion-to-evidence terminal-state model and validation tooling.
- Smoke-case specification for real Codex behavior.

### Changed

- Root may implement low-risk Direct work but remains the continuity and evidence owner.
- Explorer and Verifier are now gated instead of mandatory topology stages.
- Reviewer output is advisory findings; deterministic evidence decides the terminal state.

### Removed

- The fixed v1.1 requirement that every task follow Explorer → Implementer → Verifier.
