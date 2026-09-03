"""Conflict-safe project-scoped installer for the OpenCode overlay."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OVERLAY_ROOT = PACKAGE_ROOT / "overlay" / ".opencode"
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


def load_manifest(target: Path) -> dict[str, str]:
    path = manifest_path(target)
    if not path.is_file():
        return {}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    files = parsed.get("files", {})
    return files if isinstance(files, dict) else {}


def install(target: Path, dry_run: bool = False) -> list[Path]:
    target = target.resolve()
    planned: list[Path] = []
    for source in overlay_files():
        destination = target / ".opencode" / relative_overlay_path(source)
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
    manifest = {str(path.relative_to(target / ".opencode")): digest(path) for path in overlay_files() for path in [target / ".opencode" / relative_overlay_path(path)]}
    manifest_path(target).write_text(json.dumps({"version": "0.1.0", "files": manifest}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return planned


def uninstall(target: Path) -> tuple[list[Path], list[Path]]:
    target = target.resolve()
    known = load_manifest(target)
    removed: list[Path] = []
    preserved: list[Path] = []
    for relative, expected_digest in known.items():
        path = target / ".opencode" / relative
        if not path.exists():
            continue
        if path.is_file() and digest(path) == expected_digest:
            path.unlink()
            removed.append(path)
        else:
            preserved.append(path)
    manifest_path(target).unlink(missing_ok=True)
    return removed, preserved


def verify_install(target: Path) -> list[str]:
    root = target / ".opencode"
    required = [
        root / "commands/orchestrate.md",
        root / "agents/harness-orchestrator.md",
        root / "agents/harness-explorer.md",
        root / "agents/harness-implementer.md",
        root / "agents/harness-verifier.md",
        root / "references/orchestration-contract.md",
    ]
    errors = [f"missing required overlay file: {path}" for path in required if not path.is_file()]
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
