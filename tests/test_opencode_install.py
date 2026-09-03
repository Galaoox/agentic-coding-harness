from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = REPO_ROOT / "packages/opencode/install/install.py"
SPEC = importlib.util.spec_from_file_location("opencode_install", INSTALLER_PATH)
assert SPEC is not None and SPEC.loader is not None
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


def test_dry_run_does_not_write_and_install_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    planned = INSTALLER.install(target, dry_run=True)
    assert planned
    assert not (target / ".opencode").exists()
    installed = INSTALLER.install(target)
    assert installed == planned
    assert INSTALLER.install(target) == []


def test_install_rejects_conflicting_destination(tmp_path: Path) -> None:
    target = tmp_path / "target"
    conflict = target / ".opencode/agents/harness-explorer.md"
    conflict.parent.mkdir(parents=True)
    conflict.write_text("conflict", encoding="utf-8")
    with pytest.raises(INSTALLER.InstallConflict):
        INSTALLER.install(target)


def test_uninstall_preserves_modified_and_unrelated_files(tmp_path: Path) -> None:
    target = tmp_path / "target"
    INSTALLER.install(target)
    tracked = target / ".opencode/agents/harness-explorer.md"
    tracked.write_text(tracked.read_text(encoding="utf-8") + "\nmodified", encoding="utf-8")
    unrelated = target / ".opencode/agents/unrelated.md"
    unrelated.write_text("unrelated", encoding="utf-8")
    removed, preserved = INSTALLER.uninstall(target)
    assert removed
    assert tracked in preserved
    assert unrelated.exists()


def test_verify_install_reports_missing_command(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    errors = INSTALLER.verify_install(target)
    assert any("orchestrate" in error for error in errors)
