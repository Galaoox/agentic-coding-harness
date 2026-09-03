from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "packages/codex/skills/codex-orchestrator"
OPENCODE = ROOT / "packages/opencode/overlay/.opencode"


def test_codex_uses_modular_conditional_references() -> None:
    skill = (CODEX / "SKILL.md").read_text(encoding="utf-8")
    assert "references/orchestration-contract.md" not in skill
    assert "references/direct.md" in skill
    assert "references/standard.md" in skill
    assert "references/evidence.md" in skill
    assert "references/model-routing.md" in skill
    assert "only when `long-running` applies" in skill
    assert "only when `high-risk` applies" in skill
    assert not (CODEX / "references/orchestration-contract.md").exists()


def test_codex_reference_index_covers_routes_and_modifiers() -> None:
    index = (CODEX / "references/index.md").read_text(encoding="utf-8")
    for name in ("direct.md", "standard.md", "evidence.md", "model-routing.md", "long-running.md", "high-risk.md"):
        assert name in index


def test_codex_model_policy_caps_sol_at_high() -> None:
    policy = (CODEX / "references/model-routing.md").read_text(encoding="utf-8")
    assert "Sol" in policy
    assert "`medium`" in policy
    assert "hard ceiling" in policy
    assert "`high`" in policy
    assert "Terra" in policy and "Luna" in policy


def test_opencode_uses_self_contained_modular_references() -> None:
    root_agent = (OPENCODE / "agents/harness-orchestrator.md").read_text(encoding="utf-8")
    command = (OPENCODE / "commands/orchestrate.md").read_text(encoding="utf-8")
    assert "references/orchestration-contract.md" not in root_agent + command
    assert ".opencode/references/index.md" in root_agent + command
    assert not (OPENCODE / "references/orchestration-contract.md").exists()
    for name in ("index.md", "direct.md", "standard.md", "evidence.md", "long-running.md", "high-risk.md"):
        assert (OPENCODE / "references" / name).is_file()
