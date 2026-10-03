"""Editorial conformance checks; these do not prove model behavior."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = [ROOT / "packages/codex/skills/codex-orchestrator/references",
              ROOT / "packages/opencode/overlay/.opencode/references"]


def test_shared_contract_keeps_causal_and_evidence_invariants():
    content = (ROOT / "packages/core/contracts/evidence-driven-orchestration.md").read_text(encoding="utf-8")
    for term in ("three corrections per independent root defect", "Detection and investigation are not corrections",
                 "Changing route, actor, session", "An unresolved required defect prevents",
                 "Planning-only requests stop at plan delivery", "Root alone maintains the plan",
                 "A setup failure is not RED", "Unexpected mutations prevent acceptance"):
        assert term in content


def test_installed_adapters_specify_shared_capabilities():
    for references in REFERENCES:
        combined = "\n".join(p.read_text(encoding="utf-8") for p in references.glob("*.md"))
        assert "packages/core/" not in combined
        for term in ("three corrections per independent root defect", "never reset counts",
                     "Planning-only", "readiness is not execution authorization",
                     "one exceptional independent premise check", "deterministic scenarios",
                     "no intervening edits", "checkpoints require explicit authorization"):
            assert term.lower() in combined.lower()
        assert "Allow one scoped correction" not in combined
        direct = (references / "direct.md").read_text(encoding="utf-8")
        assert "Bounded error alone does not escalate" in direct
        assert "Reclassification consumes no correction" in direct
        assert "high-risk excludes Direct" in direct


def test_conformance_catalog_does_not_promote_static_evidence_to_behavioral_proof():
    catalog = yaml.safe_load((ROOT / "docs/knowledge-base.yaml").read_text(encoding="utf-8"))
    assert len(catalog["adapter_conformance"]) == 6
    for capability in catalog["adapter_conformance"].values():
        assert capability["codex"] == capability["opencode"] == "specified"
        assert capability["behavioral_evidence"] == "pending"


def test_standard_preserves_one_writer_and_gated_review():
    for references in REFERENCES:
        standard = (references / "standard.md").read_text(encoding="utf-8")
        assert "One Implementer" in standard
        assert "Fresh read-only Verifier" in standard
        assert "stale binding blocks affected work" in standard
        assert "required high-risk review remains" in standard
