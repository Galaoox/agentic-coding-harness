from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "packages/core/contracts/evidence-driven-orchestration.md"
CODEX_REFERENCES = REPO_ROOT / "packages/codex/skills/codex-orchestrator/references"
OPENCODE_PACKAGE = REPO_ROOT / "packages/opencode/overlay/.opencode"


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


def test_codex_references_are_self_contained_without_losing_the_contract() -> None:
    content = "\n".join(path.read_text(encoding="utf-8") for path in CODEX_REFERENCES.glob("*.md"))
    assert "packages/core/contracts/evidence-driven-orchestration.md" not in content
    for term in ("Direct", "Standard", "one Implementer", "one scoped correction", "VERIFIED_WITH_RISKS"):
        assert term in content


def test_runtime_packages_preserve_task_brief_authority_and_direct_correction() -> None:
    codex = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (REPO_ROOT / "packages/codex/skills/codex-orchestrator").rglob("*.md")
    )
    opencode = "\n".join(path.read_text(encoding="utf-8") for path in OPENCODE_PACKAGE.rglob("*.md"))
    for content in (codex, opencode):
        for term in (
            "Before editing or delegation",
            "stable criterion IDs",
            "evidence matrix",
            "candidate state",
            "route and modifiers",
            "assumptions and constraints",
            "escalation conditions",
            "memory source",
            "higher-authority current evidence",
            "FAILED pending correction",
            "promote to Standard",
            "Standard Implementer",
            "one consolidated question",
            "Completed",
            "Status",
            "Progress",
            "Next",
        ):
            assert term in content
    assert "hidden: true" in opencode
    assert "manually invocable" in opencode


def test_direct_reclassification_does_not_consume_the_correction() -> None:
    direct_files = (
        CODEX_REFERENCES / "direct.md",
        OPENCODE_PACKAGE / "references/direct.md",
    )
    for path in direct_files:
        content = path.read_text(encoding="utf-8")
        assert "During initial classification, before implementation" in content
        assert "promote to Standard without consuming the correction" in content
        assert "After implementation begins, a failed check, missing required evidence, or blocking reproducible finding" in content
        assert "FAILED pending correction" in content
