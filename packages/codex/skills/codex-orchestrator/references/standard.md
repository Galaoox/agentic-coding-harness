# Standard route

Use Standard whenever a Direct gate is false or uncertain.

```text
DEFINE → EXPLORE? → IMPLEMENT → SCOPE_AND_DETERMINISTIC_CHECKS → REVIEW? → TERMINAL
```

## Roles

- **Root:** owns acceptance, routing, state, and synthesis; does not edit implementation files.
- **Explorer:** optional, read-only, and used only for uncertainty about location, behavior, dependencies, or risk. Returns evidence, paths/symbols, risks, and a non-binding recommendation.
- **Implementer:** one Implementer is the persistent writer for all coupled source, configuration, and test changes. It cannot delegate. It returns changed files, implementation summary, criterion evidence, commands/results, and limitations.
- **Verifier:** fresh and read-only; required only for `high-risk`, unresolved material public API/architecture risk, insufficient deterministic coverage, or a concrete residual risk. Findings need reproducible evidence.

Run serially. Never fan out overlapping writers. Every delegated prompt prohibits further delegation. A correction retains the same Implementer and is limited to one blocking reproducible finding set.

Load [`model-routing.md`](model-routing.md) when assigning roles. Load modifier references only when their gates apply, then load [`evidence.md`](evidence.md) before acceptance.
