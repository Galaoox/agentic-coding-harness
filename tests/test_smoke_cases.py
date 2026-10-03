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


@pytest.mark.parametrize("terminal", [{}, [], 1, "unknown"])
def test_case_rejects_invalid_terminal(tmp_path, terminal):
    path = tmp_path / "case.json"
    path.write_text(json.dumps({"id": "invalid", "message": "check", "allowed_changes": [],
                               "checks": [["python", "-V"]], "expected_terminal": terminal}))
    with pytest.raises(ValueError, match="expected_terminal"):
        load_case(path)
