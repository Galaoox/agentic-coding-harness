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
        "three corrections per independent root defect",
        "evidence",
    ):
        assert term in content


def test_codex_references_are_self_contained_without_losing_the_contract() -> None:
    content = "\n".join(path.read_text(encoding="utf-8") for path in CODEX_REFERENCES.glob("*.md"))
    assert "packages/core/contracts/evidence-driven-orchestration.md" not in content
    for term in ("Direct", "Standard", "one Implementer", "one scoped correction", "VERIFIED_WITH_RISKS"):
        assert term in content


def test_shared_contract_preserves_causal_budgets_and_scoped_stopping() -> None:
    content = CORE.read_text(encoding="utf-8")
    for requirement in (
        "Detection and investigation are not corrections",
        "an attempted corrective change consumes one attempt",
        "Several symptoms of the same cause share one budget",
        "evidence supports their independence",
        "uncertainty about cause identity does not authorize a fresh budget",
        "before evidence, hypothesis, change, after evidence, and outcome",
        "Before each correction, record its ordinal as attempt x/3",
        "After each correction, record actual checks and outcome",
        "state the failure reason or explicitly mark the cause unknown",
        "Changing route, actor, session, label, or defect name never resets",
        "If the third correction leaves the defect unresolved, stop dependent work",
        "Unrelated work may continue only when its independence is evidenced",
        "An unresolved required defect prevents VERIFIED and VERIFIED_WITH_RISKS",
    ):
        assert requirement in content
    assert "A task permits at most one correction" not in content


def test_shared_contract_preserves_optional_planning_and_evidence_gates() -> None:
    content = CORE.read_text(encoding="utf-8")
    for requirement in (
        "A bounded error alone does not force Direct escalation",
        "cross-session continuity on either route",
        "Git checkpoints require explicit authorization",
        "There is no universal plan path or required template",
        "Planning-only requests stop at plan delivery",
        "Readiness is not execution authorization",
        "Root alone maintains the plan",
        "a missing or stale binding blocks affected work",
        "One exceptional independent premise check is permitted per change",
        "fresh read-only investigator independent of the premise's author",
        "Reproduction is recommended unless",
        "strict TDD is also explicit or project-required",
        "A setup failure is not RED",
        "Mandatory missing RED blocks dependent edits",
        "post-fix success cannot prove historical RED",
        "before and after a bounded verification batch with no intervening edits",
        "Unexpected mutations prevent acceptance",
        "deterministic scenarios and assertions govern acceptance",
        "Never run unattended production flows",
    ):
        assert requirement in content


def test_contract_catalog_discloses_adapter_gaps_and_backup_only_writing_skill() -> None:
    content = (REPO_ROOT / "docs/contracts/index.md").read_text(encoding="utf-8")
    for statement in (
        "This update defines the shared target, not adapter parity",
        "## Local workflow comparison",
        "## Adapter conformance gaps",
        "One correction total; no root-defect ledger",
        "The writing skill is backup-only",
        "Five agent files differ from the original manifest",
        "documentation/static tests constitute runtime behavioral proof",
    ):
        assert statement in content


def test_legacy_runtime_packages_preserve_task_brief_authority_and_direct_correction() -> None:
    # Shipped behavior only: these assertions do not prove shared-target conformance.
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


def test_legacy_direct_reclassification_does_not_consume_the_correction() -> None:
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
