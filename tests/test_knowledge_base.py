from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/knowledge-base.yaml"


def load_catalog() -> dict:
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))


def test_repository_has_indexed_knowledge_base() -> None:
    assert (ROOT / "docs/index.md").is_file()
    data = load_catalog()
    assert data["schema_version"] == 1
    assert set(data["supported_runtimes"]) == {"codex", "opencode"}


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
