"""Conflict-safe project-scoped installer for the OpenCode overlay."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OVERLAY_ROOT = PACKAGE_ROOT / "overlay" / ".opencode"
VERSION = (PACKAGE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
MANIFEST_NAME = ".agentic-coding-harness-opencode.json"


class InstallConflict(RuntimeError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def overlay_files() -> list[Path]:
    return sorted(path for path in OVERLAY_ROOT.rglob("*") if path.is_file())


def relative_overlay_path(source: Path) -> Path:
    return source.relative_to(OVERLAY_ROOT)


def manifest_path(target: Path) -> Path:
    return target / ".opencode" / MANIFEST_NAME


def validate_manifest_location(target: Path, overlay_root: Path) -> Path:
    path = manifest_path(target)
    if path.is_symlink():
        raise InstallConflict(f"manifest must not be a symlink: {path}")
    try:
        path.resolve().relative_to(overlay_root)
    except ValueError as exc:
        raise InstallConflict(f"manifest escapes overlay: {path}") from exc
    return path


def load_manifest(target: Path) -> dict[str, str]:
    path = manifest_path(target)
    if not path.is_file():
        return {}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    files = parsed.get("files", {})
    return files if isinstance(files, dict) else {}


def install(target: Path, dry_run: bool = False) -> list[Path]:
    target = target.resolve()
    overlay_target = target / ".opencode"
    resolved_overlay_target = overlay_target.resolve()
    try:
        resolved_overlay_target.relative_to(target)
    except ValueError as exc:
        raise InstallConflict(f"overlay root escapes target: {overlay_target}") from exc
    if overlay_target.is_symlink():
        raise InstallConflict(f"overlay root must not be a symlink: {overlay_target}")
    manifest_file = validate_manifest_location(target, resolved_overlay_target)
    planned: list[Path] = []
    for source in overlay_files():
        destination = overlay_target / relative_overlay_path(source)
        try:
            destination.resolve().relative_to(resolved_overlay_target)
        except ValueError as exc:
            raise InstallConflict(f"destination escapes overlay: {destination}") from exc
        if destination.is_symlink():
            raise InstallConflict(f"destination must not be a symlink: {destination}")
        if destination.exists():
            if not destination.is_file() or digest(destination) != digest(source):
                raise InstallConflict(f"destination differs: {destination}")
            continue
        planned.append(destination)
    if dry_run:
        return planned
    for destination in planned:
        source = OVERLAY_ROOT / destination.relative_to(target / ".opencode")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    manifest_contents = {str(path.relative_to(target / ".opencode")): digest(path) for path in overlay_files() for path in [target / ".opencode" / relative_overlay_path(path)]}
    manifest_file.write_text(json.dumps({"version": VERSION, "files": manifest_contents}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return planned


def uninstall(target: Path) -> tuple[list[Path], list[Path]]:
    target = target.resolve()
    overlay_path = target / ".opencode"
    overlay_root = overlay_path.resolve()
    try:
        overlay_root.relative_to(target)
    except ValueError as exc:
        raise InstallConflict(f"overlay root escapes target: {overlay_path}") from exc
    if overlay_path.is_symlink():
        raise InstallConflict(f"overlay root must not be a symlink: {overlay_path}")
    manifest_file = validate_manifest_location(target, overlay_root)
    known = load_manifest(target)
    removed: list[Path] = []
    preserved: list[Path] = []
    for relative, expected_digest in known.items():
        try:
            candidate = overlay_root / relative
            path = candidate.resolve()
        except TypeError:
            preserved.append(overlay_root)
            continue
        if candidate.is_symlink():
            preserved.append(candidate)
            continue
        if candidate.absolute() != path:
            preserved.append(path)
            continue
        try:
            path.relative_to(overlay_root)
        except ValueError:
            preserved.append(path)
            continue
        if not path.exists():
            continue
        if path.is_file() and digest(path) == expected_digest:
            path.unlink()
            removed.append(path)
        else:
            preserved.append(path)
    manifest_file.unlink(missing_ok=True)
    return removed, preserved


def verify_install(target: Path) -> list[str]:
    target = target.resolve()
    overlay_path = target / ".opencode"
    errors: list[str] = []
    if overlay_path.is_symlink():
        return [f"overlay root must not be a symlink: {overlay_path}"]
    overlay_root = overlay_path.resolve()
    try:
        overlay_root.relative_to(target)
        manifest_file = validate_manifest_location(target, overlay_root)
    except InstallConflict as exc:
        return [str(exc)]

    required = [
        overlay_root / "commands/orchestrate.md",
        overlay_root / "agents/harness-orchestrator.md",
        overlay_root / "agents/harness-explorer.md",
        overlay_root / "agents/harness-implementer.md",
        overlay_root / "agents/harness-verifier.md",
        overlay_root / "references/index.md",
        overlay_root / "references/direct.md",
        overlay_root / "references/standard.md",
        overlay_root / "references/evidence.md",
        overlay_root / "references/long-running.md",
        overlay_root / "references/high-risk.md",
    ]
    errors.extend(f"missing required overlay file: {path}" for path in required if not path.is_file())
    if not manifest_file.is_file():
        errors.append(f"missing install manifest: {manifest_file}")
    else:
        try:
            payload = json.loads(manifest_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid install manifest: {exc}")
        else:
            if not isinstance(payload, dict):
                errors.append("install manifest must be a mapping")
            else:
                if payload.get("version") != VERSION:
                    errors.append(f"version mismatch: manifest={payload.get('version')!r}, package={VERSION!r}")
                files = payload.get("files")
                if not isinstance(files, dict):
                    errors.append("install manifest files must be a mapping")
                else:
                    for relative, expected_digest in files.items():
                        if not isinstance(relative, str) or not isinstance(expected_digest, str):
                            errors.append("install manifest entries must map string paths to string digests")
                            continue
                        candidate = overlay_root / relative
                        resolved = candidate.resolve()
                        try:
                            resolved.relative_to(overlay_root)
                        except ValueError:
                            errors.append(f"manifest path escapes overlay: {relative}")
                            continue
                        if candidate.is_symlink():
                            errors.append(f"managed file must not be a symlink: {candidate}")
                        elif not candidate.is_file():
                            errors.append(f"missing managed overlay file: {candidate}")
                        elif digest(candidate) != expected_digest:
                            errors.append(f"digest mismatch: {candidate}")
    if not errors and "agent: harness-orchestrator" not in required[0].read_text(encoding="utf-8"):
        errors.append("orchestrate command does not select harness-orchestrator")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    try:
        if args.uninstall:
            removed, preserved = uninstall(args.target)
            print(json.dumps({"removed": [str(x) for x in removed], "preserved": [str(x) for x in preserved]}))
        else:
            print(json.dumps({"planned": [str(x) for x in install(args.target, args.dry_run)], "dry_run": args.dry_run}))
    except InstallConflict as exc:
        print(f"conflict: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
