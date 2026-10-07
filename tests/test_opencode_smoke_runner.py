from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from contextlib import contextmanager

import pytest


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


def run_cli(tmp_path, monkeypatch, capsys, *, message="VERIFIED", edit=None, checks=None, runtime="opencode", expected=None, case=True, entrypoint=None, version="opencode v2.0.24", options=None, finished=True, registered=True, cleanup=True):
    if case:
        path = tmp_path / "case.json"
        path.write_text(json.dumps({"id": "regression", "message": "{invocation} make a bounded change",
                                   "allowed_changes": ["answer.txt"],
                                   "checks": checks or [[sys.executable, "-c", "pass"]],
                                   "expected_terminal": expected}), encoding="utf-8")
    args = ["runner", "--fixture", str(tmp_path)] + (["--case", str(path)] if case else [])
    if runtime == "opencode":
        args += ["--model", "openai/gpt-6.1-sol"]
    if entrypoint:
        args += ["--entrypoint", entrypoint]
    args += options or []
    monkeypatch.setattr(sys, "argv", args)
    monkeypatch.setattr(RUNNER, "resolve_executable", lambda name: "runtime")
    real_execute = RUNNER.execute
    @contextmanager
    def private_runtime(*args):
        if not registered:
            raise ValueError("agent instructions differ")
        yield "http://127.0.0.1:9999", {}, {"instructions_and_permissions": "matched"}
        if not cleanup:
            raise ValueError("OpenCode private server cleanup failed")
    monkeypatch.setattr(RUNNER, "private_runtime", private_runtime)
    def execute(command, cwd, timeout, **kwargs):
        if command[0] != "runtime":
            return real_execute(command, cwd, timeout)
        if command[-1] == "--version":
            stdout = version
        else:
            if edit:
                (tmp_path / edit).write_text("changed", encoding="utf-8")
            events = ([{"type": "text", "part": {"text": message}}, {"type": "step_finish", "part": {"reason": "stop"}}]
                      if runtime == "opencode" else [{"type": "item.completed", "item": {"type": "agent_message", "text": message}}, {"type": "turn.completed"}])
            if not finished:
                events = events[:-1]
            stdout = "\n".join(json.dumps(event) for event in events)
        return {"command": command, "cwd": str(cwd), "exit_code": 0, "stdout": stdout, "stderr": "", "error": None}
    monkeypatch.setattr(RUNNER, "execute", execute)
    code = RUNNER.main(runtime)
    return code, json.loads(capsys.readouterr().out)


@pytest.mark.parametrize("runtime", ["opencode", "codex"])
def test_main_requires_external_success(tmp_path, monkeypatch, capsys, runtime):
    code, result = run_cli(tmp_path, monkeypatch, capsys, runtime=runtime, checks=[[sys.executable, "-c", "raise SystemExit(1)"]])
    assert code == 1
    assert result["status"] == "false_green"
    assert result["checks"][0]["exit_code"] == 1


def test_main_rejects_unauthorized_untracked_file(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys, edit="unexpected.txt")
    assert code == 1
    assert result["scope_ok"] is False
    assert result["changed_paths"] == ["unexpected.txt"]


def test_main_never_promotes_blocked_narration(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys, message="BLOCKED")
    assert code == 2
    assert result["status"] == "reported_block"
    assert result["evaluation"] == "BLOCKED"


def test_main_distinguishes_expected_block_from_functional_pass(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys, message="BLOCKED", expected="BLOCKED")
    assert code == 0
    assert result["status"] == "expected_block"
    assert result["reported_state"] == "BLOCKED"


@pytest.mark.parametrize("runtime", ["opencode", "codex"])
def test_main_accepts_measured_outcome(tmp_path, monkeypatch, capsys, runtime):
    checks = [[sys.executable, "-c", "from pathlib import Path; assert Path('answer.txt').read_text() == 'changed'"]]
    code, result = run_cli(tmp_path, monkeypatch, capsys, runtime=runtime, edit="answer.txt", checks=checks)
    assert code == 0
    assert result["status"] == "functional_pass"
    assert result["candidate_before"] != result["candidate_after"]
    assert result["verification_immutable"]


def test_main_detects_verification_mutation(tmp_path, monkeypatch, capsys):
    checks = [[sys.executable, "-c", "from pathlib import Path; Path('answer.txt').write_text('mutated')"]]
    code, result = run_cli(tmp_path, monkeypatch, capsys, checks=checks)
    assert code == 1
    assert result["status"] == "verification_mutation"


def test_main_without_case_is_only_diagnostic(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys, case=False)
    assert code == 2
    assert result["evaluation"] == "DIAGNOSTIC"


def test_opencode_entrypoint_selects_primary_without_requiring_a_prefix(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys)
    assert code == 0
    command = result["process"]["command"]
    assert command[command.index("--agent") + 1] == "harness-orchestrator"
    assert "--command" not in command
    assert "--variant" not in command
    assert "--pure" not in command
    assert "--server" in command
    assert result["registration"]["instructions_and_permissions"] == "matched"
    assert command[command.index("--model") + 1] == "openai/gpt-6.1-sol#medium"
    assert "/orchestrate" not in command[-1]
    assert result["entrypoint"] == "agent"
    assert "{invocation}" not in command[-1]


@pytest.mark.parametrize("version", ["1.18.34", "opencode v2.0.23", "opencode v3.0.0", "unknown", "opencode v2.0.24-beta"])
def test_opencode_rejects_unsupported_runtime_without_model_call(tmp_path, monkeypatch, capsys, version):
    code, result = run_cli(tmp_path, monkeypatch, capsys, version=version, edit="answer.txt")
    assert code == 2
    assert result["evaluation"] == "BLOCKED"
    assert not (tmp_path / "answer.txt").exists()


def test_opencode_registration_failure_blocks_before_model(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys, registered=False, edit="answer.txt")
    assert code == 2
    assert result["evaluation"] == "BLOCKED"
    assert "no model was invoked" in result["reason"]
    assert not (tmp_path / "answer.txt").exists()


def test_opencode_cleanup_failure_blocks_and_discloses_model_attempt(tmp_path, monkeypatch, capsys):
    code, result = run_cli(tmp_path, monkeypatch, capsys, cleanup=False, edit="answer.txt")
    assert code == 2
    assert result["evaluation"] == "BLOCKED"
    assert result["model_invocation_attempted"] is True
    assert "no model was invoked" not in result["reason"]
    assert (tmp_path / "answer.txt").exists()


def test_opencode_command_entrypoint_is_explicitly_unsupported(tmp_path, monkeypatch, capsys):
    with pytest.raises(SystemExit) as exc:
        run_cli(tmp_path, monkeypatch, capsys, entrypoint="command", edit="answer.txt")
    assert exc.value.code == 2
    assert "no --command" in capsys.readouterr().err
    assert not (tmp_path / "answer.txt").exists()


@pytest.mark.parametrize("options", [["--clean-config"], ["--model", "openai/gpt-6.1-sol#high"], ["--model", "no-provider"]])
def test_opencode_rejects_unsupported_configuration_before_execution(tmp_path, monkeypatch, capsys, options):
    with pytest.raises(SystemExit) as exc:
        run_cli(tmp_path, monkeypatch, capsys, options=options, edit="answer.txt")
    assert exc.value.code == 2
    assert not (tmp_path / "answer.txt").exists()


def test_v2_complete_token_usage_remains_separate():
    line = json.dumps({"type": "step_finish", "part": {"reason": "stop", "tokens": {
        "input": 10, "output": 20, "reasoning": 30, "cache": {"read": 40, "write": 50}}}})
    assert RUNNER.usage_metrics([line], "opencode") == {
        "input_tokens": 10, "output_tokens": 20, "reasoning_tokens": 30,
        "cached_input_tokens": 40, "cache_write_tokens": 50}


def test_v2_missing_usage_does_not_invent_worker_costs():
    metrics = RUNNER.usage_metrics(['{"type":"step_finish","part":{"tokens":{"input":12}}}'], "opencode")
    assert metrics["input_tokens"] == 12
    assert all(value is None for key, value in metrics.items() if key != "input_tokens")


def test_v2_tool_error_cannot_be_promoted_by_terminal_completion():
    trace = RUNNER.parse_jsonl([
        '{"type":"tool_use","part":{"tool":"subagent","state":{"status":"error","error":"denied"}}}',
        '{"type":"text","part":{"text":"HARNESS_STATE=VERIFIED"}}',
        '{"type":"step_finish","part":{"reason":"stop"}}'])
    assert trace.tool_calls == ["subagent"]
    assert RUNNER.classify_result(exit_code=0, trace=trace, diff_ok=True, checks_ok=True) == "trace_error"


def test_v2_reconciled_final_text_requires_external_outcome(tmp_path, monkeypatch, capsys):
    checks = [[sys.executable, "-c", "from pathlib import Path; assert Path('answer.txt').read_text() == 'changed'"]]
    code, result = run_cli(tmp_path, monkeypatch, capsys, edit="answer.txt", checks=checks, finished=False)
    assert code == 0
    assert result["status"] == "functional_pass"
    assert result["trace_complete"] is False
    assert result["completion_source"] == "cli_exit_after_session_wait"
    assert result["metrics"]["usage_complete"] is False


@pytest.mark.parametrize("defect", ["timeout", "exit", "jsonl", "terminal", "scope", "checks", "future"])
def test_v2_completion_fallback_fails_closed(defect):
    process = {"exit_code": 0, "error": None}
    trace = RUNNER.Trace([], ["HARNESS_STATE=VERIFIED"], False, [])
    version, diff_ok, checks_ok = (2, 0, 24), True, True
    if defect == "timeout":
        process["error"] = "timeout"
    elif defect == "exit":
        process["exit_code"] = 1
    elif defect == "jsonl":
        trace = trace._replace(errors=["invalid JSONL"])
    elif defect == "terminal":
        trace = trace._replace(text=["done"])
    elif defect == "scope":
        diff_ok = False
    elif defect == "checks":
        checks_ok = False
    elif defect == "future":
        version = (2, 0, 25)
    completed, source = RUNNER.completion_evidence(trace, process, version, diff_ok=diff_ok, checks_ok=checks_ok)
    assert completed.finished is False
    assert source is None


@pytest.mark.parametrize("lines", [["[]"], ['{"type":"tool","part":null}'], ["not-json"]])
def test_invalid_trace_shapes_fail_closed(lines):
    assert RUNNER.parse_jsonl(lines).errors


def test_intermediate_step_is_not_completion():
    assert not RUNNER.parse_jsonl(['{"type":"step_finish","part":{"reason":"tool-calls"}}']).finished


def test_process_timeout_is_structured(monkeypatch, tmp_path):
    import smoke_evidence
    class Process:
        count = 0
        def communicate(self, timeout):
            self.count += 1
            if self.count == 1:
                raise subprocess.TimeoutExpired("runtime", 1)
            return "partial", ""
    process = Process()
    killed = []
    monkeypatch.setattr(smoke_evidence.subprocess, "Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr(smoke_evidence, "kill_process_tree", lambda p: killed.append(p))
    result = smoke_evidence.execute(["runtime"], tmp_path, 1)
    assert result["error"] == "timeout"
    assert result["stdout"] == "partial"
    assert killed == [process]


def test_labelled_block_is_not_functional_pass():
    trace = RUNNER.Trace([], ["Terminal state: BLOCKED"], True, [])
    assert RUNNER.classify_result(exit_code=0, trace=trace, diff_ok=True, checks_ok=True) == "reported_block"


def test_absent_terminal_is_not_functional_pass():
    assert RUNNER.classify_result(exit_code=0, trace=RUNNER.Trace([], ["done"], True, []), diff_ok=True, checks_ok=True) == "missing_terminal"


def test_verification_cannot_hide_mutation_by_restoring_later(tmp_path):
    import smoke_evidence
    path = tmp_path / "answer.txt"
    path.write_text("original")
    case = {"checks": [[sys.executable, "-c", "from pathlib import Path; Path('answer.txt').write_text('changed')"],
                       [sys.executable, "-c", "from pathlib import Path; Path('answer.txt').write_text('original')"]]}
    checks, immutable = smoke_evidence.verify_case(case, tmp_path, 5)
    assert not immutable
    assert len(checks) == 1


def test_windows_launcher_resolution_avoids_posix_shim(monkeypatch):
    import smoke_evidence
    monkeypatch.setattr(smoke_evidence.os, "name", "nt")
    monkeypatch.setattr(smoke_evidence.shutil, "which", lambda name: "C:/bin/codex.cmd" if name == "codex.cmd" else None)
    assert smoke_evidence.resolve_executable("codex") == "C:/bin/codex.cmd"


def test_partial_usage_does_not_invent_missing_metrics():
    metrics = RUNNER.usage_metrics(['{"type":"turn.completed","usage":{"input_tokens":12}}'], "codex")
    assert metrics["input_tokens"] == 12
    assert metrics["output_tokens"] is None


def test_timeout_terminates_innocent_child_process(tmp_path):
    import smoke_evidence
    import time
    command = [sys.executable, "-c", "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','import time; time.sleep(8)']); time.sleep(9)"]
    started = time.monotonic()
    result = smoke_evidence.execute(command, tmp_path, 1)
    assert result["error"] == "timeout"
    assert time.monotonic() - started < 7


def test_scope_snapshot_includes_deletions_and_untracked_files(tmp_path):
    import smoke_evidence
    path = tmp_path / "before.txt"
    path.write_text("before")
    before = smoke_evidence.snapshot(tmp_path)
    path.unlink()
    (tmp_path / "after.txt").write_text("after")
    assert smoke_evidence.changed_paths(before, smoke_evidence.snapshot(tmp_path)) == ["after.txt", "before.txt"]


def test_snapshot_detects_symlink_replaced_with_regular_file(tmp_path, monkeypatch):
    import smoke_evidence
    linked = [True]
    monkeypatch.setattr(smoke_evidence.os, "walk", lambda *args, **kwargs: iter([(str(tmp_path), [], ["entry"])]))
    monkeypatch.setattr(Path, "is_symlink", lambda path: linked[0])
    monkeypatch.setattr(smoke_evidence.os, "readlink", lambda path: "target.txt")
    monkeypatch.setattr(Path, "read_bytes", lambda path: b"symlink:target.txt")
    before = smoke_evidence.snapshot(tmp_path)
    linked[0] = False
    assert smoke_evidence.changed_paths(before, smoke_evidence.snapshot(tmp_path)) == ["entry"]


def test_main_blocks_if_candidate_evidence_cannot_be_read(tmp_path, monkeypatch, capsys):
    real_snapshot = RUNNER.snapshot
    calls = [0]
    def snapshot(root):
        calls[0] += 1
        if calls[0] > 1:
            raise PermissionError("candidate unavailable")
        return real_snapshot(root)
    monkeypatch.setattr(RUNNER, "snapshot", snapshot)
    code, result = run_cli(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert result["evaluation"] == "BLOCKED"
    assert result["candidate_after"] is None
    assert result["scope_ok"] is None
    assert result["verification_immutable"] is None
