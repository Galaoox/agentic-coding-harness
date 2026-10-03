# Lightweight harness research and implementation decisions

Reviewed for the 2026-10-03 evolution. These sources provide design hypotheses;
they do not demonstrate that another harness outperforms this repository on
matched tasks, models, permissions and budgets.

## Candidate approaches

| Source | Useful design pattern | Decision for this repository |
|---|---|---|
| [Pi](https://github.com/earendil-works/pi) | Small extensible agent core; compose capabilities as needed | Preserve explicit activation and conditional references; avoid importing another orchestration layer |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | Minimal execution loop and reproducible evaluation | Add small shared outcome-checking utilities; retain independent review where the contract requires it |
| [Aider repository maps](https://aider.chat/docs/repomap.html) | Select context relevant to the task | Measure route-specific context; do not load every modifier for every task |

These are candidates for learning from, rather than a universal ranking by
installation size or token cost. This implementation adds no Python dependency.

## Evidence from companies and communities

[OpenAI harness engineering](https://openai.com/index/harness-engineering/)
supports treating repository knowledge, feedback and executable constraints as
part of the working environment. The corresponding changes here are a compact
knowledge map, complete installation inventory and executable validation.

[Anthropic's effective agents guidance](https://www.anthropic.com/engineering/building-effective-agents)
supports starting with the simplest approach that meets the task. We keep Direct
for tasks with clear gates, avoid escalating for a bounded error alone and leave
the shipped Standard ownership policy intact.

[Anthropic's agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
motivates checking outcomes separately from traces. The new runners require
external checks, scope evidence and immutable verification; a finished event or
agent-reported success cannot supply those checks.

Community discussions, including [Superpowers issue 1067](https://github.com/obra/superpowers/issues/1067),
[issue 762](https://github.com/obra/superpowers/issues/762) and a
[LocalLLaMA harness discussion](https://www.reddit.com/r/LocalLLaMA/comments/1th5t1b/favorite_agentic_coding_harness/),
were considered as qualitative signals about workflow friction and preferences.
Individual reports are not controlled comparisons. They justify testing overhead,
not removing review or changing models without candidate-specific evidence.

## Adopted changes and deferred experiment

The [implementation results](../evaluation/harness-evolution-results.md) record
portable validation, stricter manifests/permissions, six adapter specifications,
causal correction continuity, optional plans, selective global cleanup and
separate package/context/runtime metrics.

The [smoke guide](../evaluation/harness-smoke-guide.md) defines the next experiment:
same task, model, effort, checks and environment, three repetitions per variant.
Compare the existing Standard flow to a single-executor experimental profile.
Keep one writer and required independent high-risk review. This experiment is
deferred until runtime evidence is reliable; it does not change shipped roles.
