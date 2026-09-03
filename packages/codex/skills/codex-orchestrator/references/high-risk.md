# High-risk modifier

Apply only to Standard for authentication/authorization, money, migrations, secrets, PII, concurrency, infrastructure, production effects, or destructive/irreversible operations.

Required additions:

- baseline or pre-change evidence;
- rollback approach;
- isolated environment when viable;
- relevant positive and negative checks;
- a fresh Verifier after deterministic checks;
- explicit human approval before irreversible or external effects;
- Sol at `high` only when global judgment or high-risk review requires it.

A reviewer cannot authorize failed checks, scope violations, missing evidence, or absent human approval. If the required model, permission, environment, or approval is unavailable, return `BLOCKED`.
