# Long-running modifier

Apply only to Standard when work has multiple independently verifiable units or must survive a session boundary.

For each unit:

1. define unit acceptance criteria;
2. implement and run deterministic checks;
3. create a Git checkpoint or record why it is unavailable;
4. update concise versioned progress only when a later session needs it;
5. hand off base/candidate SHA, completed criteria, evidence, unresolved risks, and exactly one next unit.

Use durable `PLAN`, `RESULT`, or `REVIEW` artifacts only when cross-session continuity needs them. Do not add roles, reset context automatically, or preload full transcripts merely because work is long-running.
