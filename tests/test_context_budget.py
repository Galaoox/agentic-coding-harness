from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/report_context_budget.py"
SPEC = importlib.util.spec_from_file_location("report_context_budget", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_context_scenarios_reference_existing_files() -> None:
    report = MODULE.build_report(ROOT)
    assert report
    for scenario in report.values():
        assert scenario["files"]
        assert scenario["always"]
        assert set(scenario["files"]) == set(scenario["always"] + scenario["conditional"])
        assert scenario["bytes"] > 0
        assert scenario["lines"] > 0
        assert scenario["words"] > 0
        assert scenario["bytes"] <= scenario["max_bytes"]
        assert scenario["within_budget"] is True


def test_direct_scenarios_exclude_standard_and_modifiers() -> None:
    report = MODULE.build_report(ROOT)
    for name in ("codex-direct", "opencode-direct"):
        files = "\n".join(report[name]["files"])
        assert "standard.md" not in files
        assert "long-running.md" not in files
        assert "high-risk.md" not in files


def test_normal_standard_excludes_modifiers() -> None:
    report = MODULE.build_report(ROOT)
    for name in ("codex-standard", "opencode-standard"):
        files = "\n".join(report[name]["files"])
        assert "long-running.md" not in files
        assert "high-risk.md" not in files


def test_each_standard_modifier_has_a_budgeted_scenario_per_runtime() -> None:
    report = MODULE.build_report(ROOT)
    for name in (
        "codex-standard-long-running",
        "codex-standard-high-risk",
        "opencode-standard-long-running",
        "opencode-standard-high-risk",
    ):
        assert name in report


def test_bootstrap_agents_file_stays_compact() -> None:
    report = MODULE.build_report(ROOT)
    assert report["repository-bootstrap"]["lines"] < 100
