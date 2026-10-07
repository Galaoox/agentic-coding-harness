from __future__ import annotations

import importlib.util
import json
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


def test_install_rejects_parent_symlink_escape(tmp_path: Path) -> None:
    target = tmp_path / "target"
    outside = tmp_path / "outside"
    outside.mkdir()
    (target / ".opencode").mkdir(parents=True)
    (target / ".opencode/agents").symlink_to(outside, target_is_directory=True)

    with pytest.raises(INSTALLER.InstallConflict):
        INSTALLER.install(target)

    assert list(outside.iterdir()) == []


def test_install_rejects_manifest_symlink_escape(tmp_path: Path) -> None:
    target = tmp_path / "target"
    (target / ".opencode").mkdir(parents=True)
    victim = tmp_path / "victim.json"
    victim.write_text("preserve", encoding="utf-8")
    INSTALLER.manifest_path(target).symlink_to(victim)

    with pytest.raises(INSTALLER.InstallConflict):
        INSTALLER.install(target)

    assert victim.read_text(encoding="utf-8") == "preserve"


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


def test_uninstall_rejects_manifest_path_escape(tmp_path: Path) -> None:
    target = tmp_path / "target"
    manifest = INSTALLER.manifest_path(target)
    manifest.parent.mkdir(parents=True)
    victim = target / "victim.txt"
    victim.write_text("do not delete", encoding="utf-8")
    manifest.write_text(
        json.dumps({"version": "0.2.0", "files": {"../victim.txt": INSTALLER.digest(victim)}}),
        encoding="utf-8",
    )

    removed, preserved = INSTALLER.uninstall(target)

    assert removed == []
    assert victim.exists()
    assert victim in preserved


def test_uninstall_rejects_overlay_symlink_escape(tmp_path: Path) -> None:
    target = tmp_path / "target"
    outside = tmp_path / "outside"
    outside.mkdir()
    target.mkdir()
    (target / ".opencode").symlink_to(outside, target_is_directory=True)
    victim = outside / "victim.txt"
    victim.write_text("do not delete", encoding="utf-8")
    (outside / INSTALLER.MANIFEST_NAME).write_text(
        json.dumps({"version": "0.2.0", "files": {"victim.txt": INSTALLER.digest(victim)}}),
        encoding="utf-8",
    )

    with pytest.raises(INSTALLER.InstallConflict):
        INSTALLER.uninstall(target)

    assert victim.exists()


def test_uninstall_preserves_symlinked_manifest_entry(tmp_path: Path) -> None:
    target = tmp_path / "target"
    overlay = target / ".opencode"
    overlay.mkdir(parents=True)
    victim = overlay / "victim.txt"
    victim.write_text("do not delete", encoding="utf-8")
    link = overlay / "managed-link.md"
    link.symlink_to(victim)
    INSTALLER.manifest_path(target).write_text(
        json.dumps({"version": "0.2.0", "files": {link.name: INSTALLER.digest(victim)}}),
        encoding="utf-8",
    )

    removed, preserved = INSTALLER.uninstall(target)

    assert removed == []
    assert link in preserved
    assert link.is_symlink()
    assert victim.exists()


def test_install_writes_current_version_and_verifies_modular_references(tmp_path: Path) -> None:
    target = tmp_path / "target"
    INSTALLER.install(target)

    assert INSTALLER.verify_install(target) == []
    manifest = INSTALLER.manifest_path(target).read_text(encoding="utf-8")
    assert '"version": "0.5.0"' in manifest
    assert '"runtime_major": 2' in manifest
    for name in ("index.md", "direct.md", "standard.md", "evidence.md", "long-running.md", "high-risk.md"):
        assert (target / ".opencode/references" / name).is_file()


def test_verify_install_rejects_modified_file_and_version_drift(tmp_path: Path) -> None:
    target = tmp_path / "target"
    INSTALLER.install(target)
    installed = target / ".opencode/references/direct.md"
    installed.write_text("corrupt\n", encoding="utf-8")
    manifest_path = INSTALLER.manifest_path(target)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = "0.1.0"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = INSTALLER.verify_install(target)

    assert any("version mismatch" in error for error in errors)
    assert any("digest mismatch" in error for error in errors)


def test_verify_install_rejects_runtime_major_drift(tmp_path: Path) -> None:
    target = tmp_path / "target"
    INSTALLER.install(target)
    path = INSTALLER.manifest_path(target)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["runtime_major"] = 1
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert any("runtime major mismatch" in error for error in INSTALLER.verify_install(target))


def test_verify_install_reports_missing_command(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    errors = INSTALLER.verify_install(target)
    assert any("orchestrate" in error for error in errors)


@pytest.mark.parametrize("mutation", ["empty", "missing", "extra", "forged"])
def test_verify_rejects_incomplete_or_forged_inventory(tmp_path: Path, mutation: str) -> None:
    target = tmp_path / "target"
    INSTALLER.install(target)
    manifest_path = INSTALLER.manifest_path(target)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if mutation == "empty":
        manifest["files"] = {}
    elif mutation == "missing":
        manifest["files"].pop(next(iter(manifest["files"])))
    elif mutation == "extra":
        manifest["files"]["unrelated.md"] = "0" * 64
    else:
        path = target / ".opencode/references/direct.md"
        path.write_text("changed", encoding="utf-8")
        manifest["files"]["references/direct.md"] = INSTALLER.digest(path)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assert INSTALLER.verify_install(target)


def test_verify_allows_unmanaged_files(tmp_path: Path) -> None:
    target = tmp_path / "target"
    INSTALLER.install(target)
    (target / ".opencode/unrelated.md").write_text("personal", encoding="utf-8")
    assert INSTALLER.verify_install(target) == []
