# OpenCode v0.1 smoke cases

| ID | Case | Required observable evidence |
|---|---|---|
| O-D01 | Direct, Root-only low-risk action | custom command resolves to Root; JSONL terminal event; candidate diff/checks |
| O-S01 | Standard with uncertainty | Explorer then one Implementer task event; deterministic checks |
| O-H01 | high-risk | fresh Verifier plus explicit approval gate; no terminal VERIFIED without approval |
| O-V01 | false green | narrated PASS with failed check is classified `false_green` / failed |
| O-P01 | read-only enforcement | debug agent rejects Explorer/Verifier edit and forbidden shell writes |
| O-B01 | unavailable runtime/provider | runner returns a truthful block classification, not invented success |

Raw traces remain outside Git. A JSON event stream is observability only; deterministic checks and candidate diff decide state.
