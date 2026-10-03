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


def test_lf_budget_is_independent_of_checkout_newlines(tmp_path):
    lf, crlf = tmp_path / "lf.md", tmp_path / "crlf.md"
    lf.write_bytes(b"one\ntwo\n")
    crlf.write_bytes(b"one\r\ntwo\r\n")
    assert MODULE.measure_files([lf])["bytes"] == MODULE.measure_files([crlf])["bytes"]
    assert MODULE.measure_files([lf])["raw_bytes"] != MODULE.measure_files([crlf])["raw_bytes"]


def test_observed_roles_are_not_merged(tmp_path):
    import json
    (tmp_path / "rules.md").write_text("rules", encoding="utf-8")
    path = tmp_path / "layers.json"
    path.write_text(json.dumps([{"role": role, "layer": "global", "files": ["rules.md"]} for role in ("root", "verifier")]), encoding="utf-8")
    observations = MODULE.measure_layers(path)
    assert len(observations) == 2
    assert [entry["role"] for entry in observations] == ["root", "verifier"]


def test_direct_continuity_has_no_standard_reference():
    for runtime in ("codex", "opencode"):
        scenario = MODULE.build_report(ROOT)[runtime + "-direct-long-running"]
        assert any(path.endswith("long-running.md") for path in scenario["files"])
        assert not any(path.endswith("standard.md") for path in scenario["files"])
