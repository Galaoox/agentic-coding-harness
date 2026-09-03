from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/knowledge-base.yaml"
VALIDATOR_PATH = ROOT / "scripts/validate_knowledge_base.py"
SPEC = importlib.util.spec_from_file_location("validate_knowledge_base", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def load_catalog() -> dict:
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))


def test_repository_has_indexed_knowledge_base() -> None:
    assert (ROOT / "docs/index.md").is_file()
    data = load_catalog()
    assert data["schema_version"] == 1
    assert set(data["supported_runtimes"]) == {"codex", "opencode"}
    assert data["runtime_versions"] == {"codex": "1.3.0", "opencode": "0.2.0"}


def test_catalogued_documents_are_unique_and_exist() -> None:
    documents = load_catalog()["documents"]
    paths = [item["path"] for item in documents]
    assert len(paths) == len(set(paths))
    for item in documents:
        assert item["authority"] in {"normative", "evidence", "historical", "reference"}
        assert item["status"] in {"current", "completed", "superseded"}
        assert item["scope"]
        assert (ROOT / item["path"]).is_file(), item["path"]


def test_compact_agents_file_maps_to_current_support() -> None:
    content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert len(content.splitlines()) < 100
    assert "docs/index.md" in content
    assert "Codex is the only supported runtime" not in content
    assert "Codex" in content and "OpenCode" in content


def test_current_architecture_uses_current_runtime_versions_and_references() -> None:
    content = (ROOT / "docs/architecture.md").read_text(encoding="utf-8")
    assert "Codex v1.3" in content
    assert "OpenCode v0.2" in content
    assert "references/orchestration-contract.md" not in content


def copy_repository(tmp_path: Path) -> Path:
    destination = tmp_path / "repo"
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", ".venv", ".hermes", "__pycache__"))
    return destination


def test_validator_rejects_unindexed_normative_document(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    (root / "docs/contracts/unindexed.md").write_text("# Unindexed normative contract\n", encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("normative document is not catalogued" in error for error in errors)


def test_validator_rejects_context_over_budget(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    catalog = yaml.safe_load((root / "docs/knowledge-base.yaml").read_text(encoding="utf-8"))
    catalog["context_scenarios"]["repository-bootstrap"]["max_bytes"] = 1
    (root / "docs/knowledge-base.yaml").write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("exceeds max_bytes" in error for error in errors)


def test_validator_rejects_unindexed_knowledge_document(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    (root / "docs/evaluation/unindexed.md").write_text("# Unindexed evidence\n", encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("knowledge document is not catalogued" in error for error in errors)


def test_validator_rejects_machine_local_paths(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    architecture = root / "docs/architecture.md"
    architecture.write_text(architecture.read_text(encoding="utf-8") + "\n/home/example/private\n", encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("machine-local path" in error for error in errors)


def test_validator_rejects_unresolved_placeholders(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    architecture = root / "docs/architecture.md"
    architecture.write_text(architecture.read_text(encoding="utf-8") + "\n[SKILL_PRUNED]\n", encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("unresolved placeholder" in error for error in errors)


def test_validator_rejects_missing_runtime_support_marker(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    architecture = root / "docs/architecture.md"
    architecture.write_text(architecture.read_text(encoding="utf-8").replace("<!-- supported-runtimes: codex, opencode -->\n", ""), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("runtime support marker" in error for error in errors)


def test_validator_rejects_broken_runtime_package_link(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    routing = root / "packages/codex/skills/codex-orchestrator/references/model-routing.md"
    routing.write_text(routing.read_text(encoding="utf-8").replace("model-routing.yaml", "missing.yaml"), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("broken runtime package link" in error for error in errors)


def test_validator_rejects_catalog_path_escape(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    catalog_path = root / "docs/knowledge-base.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    catalog["documents"].append({"path": "../../outside.md", "authority": "reference", "status": "current", "scope": "repository"})
    catalog_path.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("catalogued path escapes repository" in error for error in errors)


def test_validator_rejects_context_path_escape(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    catalog_path = root / "docs/knowledge-base.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    catalog["context_scenarios"]["repository-bootstrap"]["always"] = ["/etc/hosts"]
    catalog_path.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("context path escapes repository" in error for error in errors)


def test_validator_rejects_runtime_version_drift(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    catalog_path = root / "docs/knowledge-base.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    catalog["runtime_versions"]["opencode"] = "9.9.9"
    catalog_path.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("runtime version drift" in error for error in errors)


def test_validator_reports_invalid_codex_version_metadata(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    skill = root / "packages/codex/skills/codex-orchestrator/SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8").replace('version: "1.3.0"', "version: ["), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("cannot read Codex runtime version" in error for error in errors)


def test_validator_reports_malformed_catalog_types_without_raising(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    catalog_path = root / "docs/knowledge-base.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    catalog["supported_runtimes"] = [{"codex": True}, "opencode"]
    catalog["context_scenarios"] = {1: {"always": [{}], "conditional": [], "max_bytes": 1}}
    catalog_path.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("supported_runtimes" in error for error in errors)
    assert any("scenario names" in error for error in errors)


def test_validator_rejects_document_link_outside_repository(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    architecture = root / "docs/architecture.md"
    architecture.write_text(architecture.read_text(encoding="utf-8") + "\n[outside](/etc/hosts)\n", encoding="utf-8")

    errors = VALIDATOR.validate_knowledge_base(root)

    assert any("local link escapes repository" in error for error in errors)
