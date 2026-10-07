from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate_harness_packages.py"
SPEC = importlib.util.spec_from_file_location("validate_harness_packages", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def copy_packages(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "packages", root / "packages")
    return root


def test_validates_repository_opencode_package() -> None:
    assert VALIDATOR.validate_opencode_package(REPO_ROOT) == []


@pytest.mark.parametrize("shell", [
    [{"action": "shell", "resource": "*", "effect": "allow"}],
    [{"action": "shell", "resource": "*", "effect": "ask"}, {"action": "shell", "resource": "python *", "effect": "allow"}],
])
def test_rejects_expanded_verifier_shell(tmp_path: Path, shell) -> None:
    root = copy_packages(tmp_path)
    path = root / "packages/opencode/overlay/.opencode/agents/harness-verifier.md"
    _, metadata, body = path.read_text(encoding="utf-8").split("---", 2)
    data = yaml.safe_load(metadata)
    data["permissions"] = [rule for rule in data["permissions"] if rule["action"] != "shell"] + shell
    path.write_text("---\n" + yaml.safe_dump(data) + "---" + body, encoding="utf-8")
    assert any("shell allowlist" in error for error in VALIDATOR.validate_opencode_package(root))


def test_rejects_command_with_missing_agent(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    command = root / "packages/opencode/overlay/.opencode/commands/orchestrate.md"
    command.write_text(command.read_text(encoding="utf-8").replace("harness-orchestrator", "missing-agent", 1), encoding="utf-8")
    assert any("command agent" in error for error in VALIDATOR.validate_opencode_package(root))


def test_rejects_writer_permission_for_explorer(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    explorer = root / "packages/opencode/overlay/.opencode/agents/harness-explorer.md"
    explorer.write_text(explorer.read_text(encoding="utf-8").replace('action: edit, resource: "*", effect: deny', 'action: edit, resource: "*", effect: allow'), encoding="utf-8")
    assert any("harness-explorer" in error and "edit" in error for error in VALIDATOR.validate_opencode_package(root))


def test_rejects_non_allowlisted_root_subagent(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    root_agent = root / "packages/opencode/overlay/.opencode/agents/harness-orchestrator.md"
    root_agent.write_text(root_agent.read_text(encoding="utf-8").replace('resource: harness-verifier', 'resource: general'), encoding="utf-8")
    assert any("subagent allowlist" in error for error in VALIDATOR.validate_opencode_package(root))


def test_rejects_later_permission_override(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    path = root / "packages/opencode/overlay/.opencode/agents/harness-orchestrator.md"
    _, metadata, body = path.read_text(encoding="utf-8").split("---", 2)
    data = yaml.safe_load(metadata)
    data["permissions"].append({"action": "subagent", "resource": "*", "effect": "allow"})
    path.write_text("---\n" + yaml.safe_dump(data) + "---" + body, encoding="utf-8")
    assert any("subagent allowlist" in error for error in VALIDATOR.validate_opencode_package(root))


def test_rejects_legacy_permissions_and_hidden_worker(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    path = root / "packages/opencode/overlay/.opencode/agents/harness-explorer.md"
    _, metadata, body = path.read_text(encoding="utf-8").split("---", 2)
    data = yaml.safe_load(metadata)
    data["hidden"] = True
    data["permission"] = {"edit": "deny"}
    path.write_text("---\n" + yaml.safe_dump(data) + "---" + body, encoding="utf-8")
    errors = VALIDATOR.validate_opencode_package(root)
    assert any("native V2" in error for error in errors)
    assert any("catalog" in error for error in errors)


def test_rejects_local_path_and_codex_metadata(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    evidence = root / "packages/opencode/overlay/.opencode/references/evidence.md"
    evidence.write_text(evidence.read_text(encoding="utf-8") + "\n/home/example/private\n", encoding="utf-8")
    (root / "packages/opencode/overlay/.opencode/agents/openai.yaml").write_text("x", encoding="utf-8")
    errors = VALIDATOR.validate_opencode_package(root)
    assert any("machine-local path" in error for error in errors)
    assert any("Codex metadata" in error for error in errors)


def test_rejects_contract_reference_outside_installed_overlay(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    index = root / "packages/opencode/overlay/.opencode/references/index.md"
    index.write_text(index.read_text(encoding="utf-8") + "\n[external](../../../../core/contracts/evidence-driven-orchestration.md)\n", encoding="utf-8")
    assert any("escapes installed overlay" in error for error in VALIDATOR.validate_opencode_package(root))


def test_rejects_missing_reference_inside_installed_overlay(tmp_path: Path) -> None:
    root = copy_packages(tmp_path)
    index = root / "packages/opencode/overlay/.opencode/references/index.md"
    index.write_text(index.read_text(encoding="utf-8") + "\n[missing](missing.md)\n", encoding="utf-8")
    assert any("missing markdown reference" in error for error in VALIDATOR.validate_opencode_package(root))
