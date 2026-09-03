# Codex model and reasoning routing

Model tier and reasoning effort are independent. Choose the least costly configuration likely to produce accepted candidate-specific evidence. [`model-routing.yaml`](model-routing.yaml) is the machine-readable mirror enforced by package validation; keep this guidance consistent with it.

| Work | Model | Initial effort |
|---|---|---|
| Root planning/orchestration | Sol | `medium` |
| Material architecture, security, global ambiguity, or high-risk review | Sol | `high` |
| Mechanical, repetitive, strongly checked implementation | Luna | `medium` or `high` |
| Everyday Standard implementation or exploration | Terra | `medium` |
| Difficult bounded debugging, investigation, or normal fresh verification | Terra | `high` |

Sol `high` is the hard ceiling. Do not configure or recommend a higher Sol effort.

Raise effort only when the current frame is sound but checking/depth is insufficient. Change model when the worker chose the wrong frame or lacks required judgment. Failed deterministic evidence triggers correction, escalation, or a terminal failure—not a narrative override.

Probe actual model availability in the active Codex runtime. Missing required capability yields `BLOCKED`; do not silently substitute a weaker high-risk reviewer.
