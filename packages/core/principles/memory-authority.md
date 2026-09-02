# Memory authority

Engram and other memory providers are continuity and discovery layers.

A retrieved memory is a lead. Before acting on it, the agent must verify it against the current request, repository state, tests, policies, and versioned decisions.

## Retrieve memory when

- work continues from an earlier session;
- a prior decision or rejected attempt affects the task;
- a recurring defect may have an existing diagnosis;
- context is handed to a fresh agent;
- current code does not explain why a design exists.

## Save durable knowledge when

- an architectural decision and its rationale were established;
- a rejected alternative produced a reusable lesson;
- a non-obvious root cause was verified;
- a durable project or user constraint was learned;
- a complex or unfinished task needs a handoff.

Do not use memory as a transcript sink. Do not save raw logs, obvious code facts, unverified conclusions, or transient status already represented by Git.

When a memory conflicts with a higher-authority source, follow the current source and update or supersede the stale memory.
