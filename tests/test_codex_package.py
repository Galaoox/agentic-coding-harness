from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pytest
import yaml


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


def test_codex_model_policy_is_machine_readable() -> None:
    policy_path = REPO_ROOT / "packages/codex/skills/codex-orchestrator/references/model-routing.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    assert policy["models"]["sol"]["default_effort"] == "medium"
    assert policy["models"]["sol"]["max_effort"] == "high"
    assert policy["models"]["terra"]["default_role"] == "standard-engineering"
    assert policy["models"]["luna"]["default_role"] == "mechanical-checked-work"


def test_rejects_sol_effort_above_high(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    policy_path = root / "packages/codex/skills/codex-orchestrator/references/model-routing.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    policy["models"]["sol"]["max_effort"] = "max"
    policy_path.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")

    errors = run_validation(root)

    assert any("Sol max_effort must be high" in error for error in errors)


def test_rejects_sol_default_effort_other_than_medium(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    policy_path = root / "packages/codex/skills/codex-orchestrator/references/model-routing.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    policy["models"]["sol"]["default_effort"] = "high"
    policy_path.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")

    errors = run_validation(root)

    assert any("Sol default_effort must be medium" in error for error in errors)


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
    skill.write_text(skill.read_text().replace("references/direct.md", "references/missing.md", 1))

    errors = run_validation(root)

    assert any("missing local markdown reference" in error.lower() for error in errors)


def test_rejects_legacy_route_terms(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    evidence = root / "packages/codex/skills/codex-orchestrator/references/evidence.md"
    evidence.write_text(evidence.read_text() + "\nThe atomic route applies here.\n")

    errors = run_validation(root)

    assert any("legacy route term" in error.lower() for error in errors)


def test_rejects_local_home_paths(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    evidence = root / "packages/codex/skills/codex-orchestrator/references/evidence.md"
    evidence.write_text(evidence.read_text() + "\n/home/example/private\n")

    errors = run_validation(root)

    assert any("machine-local path" in error.lower() for error in errors)


def test_rejects_missing_required_vocabulary(tmp_path: Path) -> None:
    root = copy_package(tmp_path)
    references = root / "packages/codex/skills/codex-orchestrator"
    for path in references.rglob("*.md"):
        path.write_text(path.read_text().replace("VERIFIED_WITH_RISKS", "RISKY"))

    errors = run_validation(root)

    assert any("required term" in error.lower() for error in errors)
