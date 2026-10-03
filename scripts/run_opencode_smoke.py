"""Bounded OpenCode/Codex smoke evaluation; narration never replaces outcome checks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import NamedTuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from smoke_evidence import changed_paths, execute, identity, load_case, reported_state, resolve_executable, scope_ok, snapshot, verify_case


class Trace(NamedTuple):
    tool_calls: list[str]
    text: list[str]
    finished: bool
    errors: list[str]


def parse_jsonl(lines: list[str], runtime: str = "opencode") -> Trace:
    tools, messages, errors = [], [], []
    finished = False
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append("invalid JSONL event")
            continue
        if not isinstance(event, dict):
            errors.append("JSONL event must be an object")
            continue
        kind = event.get("type")
        part = event.get("part", {}) if runtime == "opencode" else event.get("item", {})
        if not isinstance(part, dict):
            errors.append("invalid event payload")
            continue
        if kind in {"tool", "tool_use"}:
            name = part.get("tool") or part.get("name")
            if isinstance(name, str):
                tools.append(name)
            else:
                errors.append("tool event without tool name")
            state = part.get("state", {})
            if isinstance(state, dict) and state.get("status") == "error":
                errors.append(str(state.get("error", "tool error")))
        elif kind == "text" and isinstance(part.get("text"), str):
            messages.append(part["text"])
        elif kind == "step_finish":
            finished = part.get("reason") in {"stop", "end_turn"}
        elif kind == "item.completed":
            if part.get("type") == "agent_message" and isinstance(part.get("text"), str):
                messages.append(part["text"])
            elif part.get("type") in {"command_execution", "file_change", "mcp_tool_call"}:
                tools.append(part["type"])
            elif part.get("type") == "collab_tool_call":
                tools.append(str(part.get("tool", "collab_tool_call")))
        elif kind == "turn.completed":
            finished = True
        elif kind in {"error", "tool_error", "turn.failed"}:
            errors.append(str(part.get("error") or event.get("error") or kind))
    return Trace(tools, messages, finished, errors)


def classify_result(*, exit_code: int | None, trace: Trace, diff_ok: bool, checks_ok: bool) -> str:
    state = reported_state(trace.text)
    if state in {"VERIFIED", "VERIFIED_WITH_RISKS"} and (not diff_ok or not checks_ok):
        return "false_green"
    if exit_code != 0:
        return "infra_block"
    if trace.errors:
        return "trace_error"
    if not trace.finished:
        return "incomplete"
    if not diff_ok:
        return "scope_violation"
    if state in {"BLOCKED", "FAILED"}:
        return "reported_block" if state == "BLOCKED" else "reported_failure"
    if not checks_ok:
        return "check_failure"
    if state is None:
        return "missing_terminal"
    return "functional_pass"


def usage_metrics(lines: list[str], runtime: str) -> dict:
    totals = {"input_tokens": 0, "output_tokens": 0, "cached_input_tokens": 0}
    observed = {key: False for key in totals}
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if runtime == "codex" and event.get("type") == "turn.completed":
            usage = event.get("usage", {})
        elif runtime == "opencode" and event.get("type") == "step_finish":
            part = event.get("part", {})
            tokens = part.get("tokens", {}) if isinstance(part, dict) else {}
            if not isinstance(tokens, dict):
                continue
            cache = tokens.get("cache", {})
            usage = {"input_tokens": tokens.get("input"), "output_tokens": tokens.get("output"),
                     "cached_input_tokens": cache.get("read") if isinstance(cache, dict) else None}
        else:
            continue
        if isinstance(usage, dict):
            for key in totals:
                value = usage.get(key)
                if type(value) is int and value >= 0:
                    totals[key] += value
                    observed[key] = True
    return {key: value if observed[key] else None for key, value in totals.items()}


def main(runtime: str = "opencode") -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--" + runtime, default=runtime, dest="executable")
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--message", default=None)
    parser.add_argument("--case", type=Path)
    parser.add_argument("--output", type=Path, help="write UTF-8 result outside the fixture")
    parser.add_argument("--model")
    parser.add_argument("--clean-config", action="store_true", help="Codex ignores user config; OpenCode disables external plugins (global rules may remain)")
    parser.add_argument("--effort", choices=("medium", "high"), default="medium")
    parser.add_argument("--timeout", type=int, default=120, help="hard per-process time budget in seconds")
    args = parser.parse_args()
    if args.timeout < 1 or args.timeout > 600:
        parser.error("timeout must be between 1 and 600 seconds")
    try:
        case = load_case(args.case) if args.case else None
        root = args.fixture.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("fixture must be a directory")
        if args.output and args.output.resolve().is_relative_to(root):
            raise ValueError("result output must be outside the candidate fixture")
        before = snapshot(root)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid_case", "evaluation": "BLOCKED", "reason": str(exc)}))
        return 2
    executable = resolve_executable(args.executable)
    if executable is None:
        print(json.dumps({"status": "infra_block", "evaluation": "BLOCKED", "reason": runtime + " executable unavailable"}))
        return 2
    message = args.message or (case["message"] if case else "Classify this as Direct and make no edits. Return BLOCKED if required evidence is unavailable.")
    invocation = "$codex-orchestrator" if runtime == "codex" else "/orchestrate"
    message = message.replace("{invocation}", invocation)
    message += "\nEnd your final response with HARNESS_STATE=VERIFIED, VERIFIED_WITH_RISKS, FAILED or BLOCKED as applicable."
    if runtime == "opencode":
        command = [executable, "run", "--command", "orchestrate", "--format", "json", "--variant", args.effort]
        if args.clean_config:
            command.append("--pure")
        if args.model:
            command += ["--model", args.model]
    else:
        command = [executable, "exec", "--json", "--ephemeral", "--sandbox", "workspace-write",
                   "-c", 'approval_policy="never"', "-c", 'model_reasoning_effort="' + args.effort + '"']
        if args.clean_config:
            command.append("--ignore-user-config")
        if args.model:
            command += ["--model", args.model]
    command.append(message)
    started = time.monotonic()
    version = execute([executable, "--version"], root, min(args.timeout, 15))
    process = execute(command, root, args.timeout)
    lines = [line for line in process["stdout"].splitlines() if line.strip()]
    trace = parse_jsonl(lines, runtime)
    evidence_error = None
    try:
        after = snapshot(root)
        checks, immutable = verify_case(case, root, args.timeout) if case and process["error"] is None else ([], True)
    except OSError as exc:
        after, checks, immutable = {}, [], True
        evidence_error = str(exc)
    changes = changed_paths(before, after)
    diff_ok = scope_ok(changes, case["allowed_changes"]) if case else not changes
    checks_ok = bool(checks) and immutable and all(check["exit_code"] == 0 and check["error"] is None for check in checks)
    status = "infra_block" if evidence_error else process["error"] or classify_result(exit_code=process["exit_code"], trace=trace, diff_ok=diff_ok, checks_ok=checks_ok)
    state = reported_state(trace.text)
    expected = case.get("expected_terminal") if case else None
    if not case and status not in {"timeout", "infra_block", "trace_error", "incomplete"}:
        status = "diagnostic_only"
    elif expected in {"BLOCKED", "FAILED"} and state == expected and diff_ok and checks_ok and trace.finished and not trace.errors and process["exit_code"] == 0:
        status = "expected_block" if expected == "BLOCKED" else "expected_failure"
    elif expected and state != expected and status == "functional_pass":
        status = "terminal_mismatch"
    if not immutable:
        status = "verification_mutation"
    passed = status in {"functional_pass", "expected_block", "expected_failure"}
    metrics = usage_metrics(lines, runtime)
    metrics.update({"duration_seconds": round(time.monotonic() - started, 3), "tool_calls": len(trace.tool_calls),
                    "delegations": trace.tool_calls.count("task") if runtime == "opencode" else trace.tool_calls.count("spawn_agent") if "spawn_agent" in trace.tool_calls else None,
                    "corrections": None, "human_interventions": None})
    result = {"status": status, "evaluation": "PASS" if passed else "DIAGNOSTIC" if not case else "BLOCKED" if status in {"infra_block", "timeout", "reported_block"} else "FAIL",
              "runtime": runtime, "runtime_version": version["stdout"].strip(), "model": args.model,
              "effort": args.effort, "timeout_seconds": args.timeout, "case": case["id"] if case else None,
              "clean_config": args.clean_config,
              "candidate_before": identity(before), "candidate_after": None if evidence_error else identity(after), "changed_paths": changes if not evidence_error else None,
              "scope_ok": None if evidence_error else diff_ok, "checks": checks, "verification_immutable": None if evidence_error else immutable,
              "reported_state": state, "tools": trace.tool_calls, "text": trace.text, "errors": trace.errors,
              "process": process, "evidence_error": evidence_error, "metrics": metrics}
    serialized = json.dumps(result, ensure_ascii=False)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
        print(json.dumps({key: result[key] for key in ("status", "evaluation", "runtime", "case", "reported_state", "metrics")}))
    else:
        print(serialized)
    return 0 if passed else 2 if status in {"infra_block", "timeout", "reported_block", "diagnostic_only"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
