# Harness evolution implementation

Implement the approved audit for team use and CI, preserving explicit activation,
two routes, one writer, and gated independent review. External harnesses supply
design hypotheses, not demonstrated superiority.

## Work units

| Unit | Acceptance | Rollback boundary | State |
|---|---|---|---|
| Validation | POSIX catalog identity, Windows/Linux CI, complete permissions and install inventory | Validators, installer, associated tests and CI | Implemented; local Windows checks pass; remote CI pending |
| Evidence | External case assertions, candidate snapshots, bounded process errors, both runtime adapters | Smoke runners, case fixtures and regression tests | Implemented; live trials and release limits recorded |
| Conformance | Six shared capabilities reflected in self-contained adapters and versions | Runtime references, catalog, conformance tests and docs | Specification implemented; full model-backed conformance pending |
| Context | LF-normalized package metrics, explicit layers/roles and run metrics | Context report, tests and measurement docs | Implemented; budgets pass; A/B experiment deferred |
| Cleanup | Remove only authorized Gentle markers, preserve remaining bytes | Restore per-file external backup | Completed |

## Authorization and evidence

The user requested implementation and authorized removal of the Gentle trigger
block in global Codex instructions and the Gentle CodeGraph block in global
OpenCode instructions. RTK and advisor instructions remain. Backups live beside
each original file with suffix `.before-harness-cleanup-20261003`.

Baseline: commit `01e95cf`; 64 passed, one optional fixture skipped. Knowledge and
combined validators fail on Windows path separators. Package context budgets
pass. `.atl/` is unrelated user work. No commits or publication are required.

Checks and runtime evidence are recorded in the [evaluation results](../../evaluation/harness-evolution-results.md).
The implementation is complete. The plan stays active for the remaining release
evidence: remote Windows/Linux CI execution, full model-backed conformance and
the later matched delegation experiment. Live blockers are disclosed separately
from deterministic checks.
