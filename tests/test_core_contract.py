from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "packages/core/contracts/evidence-driven-orchestration.md"
CODEX = REPO_ROOT / "packages/codex/skills/codex-orchestrator/references/orchestration-contract.md"


def test_core_contract_defines_shared_invariants() -> None:
    content = CORE.read_text(encoding="utf-8")
    for term in (
        "Direct",
        "Standard",
        "long-running",
        "high-risk",
        "VERIFIED",
        "VERIFIED_WITH_RISKS",
        "FAILED",
        "BLOCKED",
        "one writer",
        "one correction",
        "evidence",
    ):
        assert term in content


def test_codex_contract_links_to_shared_core_without_losing_its_contract() -> None:
    content = CODEX.read_text(encoding="utf-8")
    assert "packages/core/contracts/evidence-driven-orchestration.md" in content
    assert "Codex-specific mechanics remain normative" in content
