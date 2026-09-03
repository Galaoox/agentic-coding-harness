# High-risk modifier

Apply only to Standard for authentication/authorization, money, migrations, secrets, PII, concurrency, infrastructure, production effects, or destructive/irreversible operations.

Require baseline evidence, rollback, isolation when viable, relevant positive/negative checks, a fresh Verifier after deterministic checks, and human approval before irreversible/external effects.

A reviewer cannot authorize failed checks, scope violations, missing evidence, or absent approval. Missing required capability yields `BLOCKED`.
