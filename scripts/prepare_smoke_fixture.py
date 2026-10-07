"""Prepare a fresh disposable project with the exact candidate runtime package."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def prepare(target: Path, runtime: str, case: str | None = None) -> None:
    if runtime not in {"codex", "opencode"}:
        raise ValueError("unsupported runtime")
    if case is not None and not (ROOT / "tests/fixtures/harness-smoke/cases" / (case + ".json")).is_file():
        raise ValueError("unknown smoke case")
    target = target.resolve()
    if target.exists():
        raise FileExistsError("fixture target must not already exist")
    shutil.copytree(ROOT / "tests/fixtures/harness-smoke/project", target)
    if case is not None and case != "causal-continuity":
        (target / "brief.json").unlink()
    if case == "high-risk":
        shutil.copy2(ROOT / "tests/fixtures/harness-smoke/high-risk/test_high_risk_acceptance.py.template",
                     target / "test_high_risk_acceptance.py")
    if runtime == "codex":
        shutil.copytree(ROOT / "packages/codex/skills/codex-orchestrator", target / ".agents/skills/codex-orchestrator")
    else:
        path = ROOT / "packages/opencode/install/install.py"
        spec = importlib.util.spec_from_file_location("smoke_overlay_install", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.install(target)
    subprocess.run(["git", "init", "--quiet", str(target)], check=True, timeout=15)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--runtime", choices=("codex", "opencode"), required=True)
    parser.add_argument("--case", help="case id; isolate exhausted correction history to causal-continuity")
    args = parser.parse_args()
    try:
        prepare(args.target, args.runtime, args.case)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "infra_block", "reason": str(exc)}))
        return 2
    print(json.dumps({"fixture": str(args.target.resolve()), "runtime": args.runtime, "status": "prepared"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
