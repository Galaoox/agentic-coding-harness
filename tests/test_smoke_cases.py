from pathlib import Path
import shutil
import subprocess
import sys
import json

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_smoke_fixture import prepare
from smoke_evidence import load_case


def test_cases_are_externally_verifiable():
    cases = list((ROOT / "tests/fixtures/harness-smoke/cases").glob("*.json"))
    assert len(cases) == 8
    for path in cases:
        case = load_case(path)
        assert case["checks"]
        assert case["expected_terminal"]


@pytest.mark.parametrize("runtime", ["codex", "opencode"])
def test_prepare_installs_candidate_and_refuses_overwrite(tmp_path, runtime):
    target = tmp_path / runtime
    prepare(target, runtime)
    assert (target / ".git").is_dir()
    assert (target / "calculator.py").is_file()
    package = target / (".agents/skills/codex-orchestrator/SKILL.md" if runtime == "codex" else ".opencode/commands/orchestrate.md")
    assert package.is_file()
    with pytest.raises(FileExistsError):
        prepare(target, runtime)


def test_fixture_outcome_checks_detect_bug_and_accept_expected_block(tmp_path):
    target = tmp_path / "project"
    shutil.copytree(ROOT / "tests/fixtures/harness-smoke/project", target)
    assert subprocess.run([sys.executable, "check_outcome.py", "direct"], cwd=target, capture_output=True).returncode == 1
    assert subprocess.run([sys.executable, "check_outcome.py", "causal"], cwd=target, capture_output=True).returncode == 0
    path = target / "calculator.py"
    path.write_text(path.read_text().replace("return a - b", "return a + b"))
    assert subprocess.run([sys.executable, "check_outcome.py", "direct"], cwd=target, capture_output=True).returncode == 0


@pytest.mark.parametrize("expression,expected_exit", [("token == 'valid'", 1),
                                                     ("type(token) is str and token == 'valid'", 0)])
def test_high_risk_acceptance_rejects_custom_equality_bypass(tmp_path, expression, expected_exit):
    target = tmp_path / "project"
    shutil.copytree(ROOT / "tests/fixtures/harness-smoke/project", target)
    path = target / "calculator.py"
    path.write_text(path.read_text().replace("return True", "return " + expression))
    result = subprocess.run([sys.executable, "-B", "check_outcome.py", "high-risk"], cwd=target, capture_output=True)
    assert result.returncode == expected_exit


@pytest.mark.parametrize("case", ["direct", "standard", "high-risk", "causal-continuity"])
def test_case_preparation_isolates_exhausted_history(tmp_path, case):
    target = tmp_path / case
    prepare(target, "opencode", case)
    assert (target / "brief.json").exists() == (case == "causal-continuity")
    assert (target / "test_high_risk_acceptance.py").exists() == (case == "high-risk")


@pytest.mark.parametrize("terminal", [{}, [], 1, "unknown"])
def test_case_rejects_invalid_terminal(tmp_path, terminal):
    path = tmp_path / "case.json"
    path.write_text(json.dumps({"id": "invalid", "message": "check", "allowed_changes": [],
                               "checks": [["python", "-V"]], "expected_terminal": terminal}))
    with pytest.raises(ValueError, match="expected_terminal"):
        load_case(path)
