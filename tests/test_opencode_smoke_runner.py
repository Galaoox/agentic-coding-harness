from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts/run_opencode_smoke.py"
SPEC = importlib.util.spec_from_file_location("run_opencode_smoke", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def test_parse_jsonl_extracts_tools_and_terminal_text() -> None:
    events = [
        '{"type":"tool","part":{"tool":"task"}}',
        '{"type":"tool_use","part":{"type":"tool","tool":"read"}}',
        '{"type":"text","part":{"text":"VERIFIED"}}',
        '{"type":"step_finish","part":{"reason":"stop"}}',
    ]
    trace = RUNNER.parse_jsonl(events)
    assert trace.tool_calls == ["task", "read"]
    assert trace.text == ["VERIFIED"]
    assert trace.finished is True


def test_parse_jsonl_fails_closed_on_invalid_json() -> None:
    trace = RUNNER.parse_jsonl(["not-json"])
    assert trace.errors


def test_classify_requires_evidence_over_narration() -> None:
    result = RUNNER.classify_result(exit_code=0, trace=RUNNER.Trace([], ["VERIFIED"], True, []), diff_ok=False, checks_ok=False)
    assert result == "false_green"
