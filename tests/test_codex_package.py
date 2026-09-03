from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate_codex_package.py"
SPEC = importlib.util.spec_from_file_location("validate_codex_package", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def copy_package(tmp_path: Path) -> Path:
    destination = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "packages", destination / "packages")
    return destination


def run_validation(root: Path):
    return VALIDATOR.validate_package(root)


def test_validates_the_repository_codex_package() -> None:
    assert run_validation(REPO_ROOT) == []


def test_rejects_invalid_skill_frontmatter(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    skill = root / "packages/codex/skills/codex-orchestrator/SKILL.md"
    skill.write_text(skill.read_text().replace("name: codex-orchestrator", "name: ["))

    errors = run_validation(root)

    assert any("frontmatter" in error.lower() for error in errors)


def test_rejects_implicit_invocation(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    metadata = root / "packages/codex/skills/codex-orchestrator/agents/openai.yaml"
    metadata.write_text(metadata.read_text().replace("allow_implicit_invocation: false", "allow_implicit_invocation: true"))

    errors = run_validation(root)

    assert any("allow_implicit_invocation" in error for error in errors)


def test_rejects_missing_local_markdown_reference(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    skill = root / "packages/codex/skills/codex-orchestrator/SKILL.md"
    skill.write_text(skill.read_text().replace("references/orchestration-contract.md", "references/missing.md", 1))

    errors = run_validation(root)

    assert any("missing local markdown reference" in error.lower() for error in errors)


def test_rejects_legacy_route_terms(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    contract = root / "packages/codex/skills/codex-orchestrator/references/orchestration-contract.md"
    contract.write_text(contract.read_text() + "\nThe atomic route applies here.\n")

    errors = run_validation(root)

    assert any("legacy route term" in error.lower() for error in errors)


def test_rejects_local_home_paths(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    contract = root / "packages/codex/skills/codex-orchestrator/references/orchestration-contract.md"
    contract.write_text(contract.read_text() + "\n/home/example/private\n")

    errors = run_validation(root)

    assert any("machine-local path" in error.lower() for error in errors)


def test_rejects_missing_required_vocabulary(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    contract = root / "packages/codex/skills/codex-orchestrator/references/orchestration-contract.md"
    contract.write_text(contract.read_text().replace("`VERIFIED_WITH_RISKS`", "`RISKY`"))

    errors = run_validation(root)

    assert any("required term" in error.lower() for error in errors)
