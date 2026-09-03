"""Observable OpenCode smoke runner; raw traces are intentionally not written to Git."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from typing import NamedTuple
from pathlib import Path


class Trace(NamedTuple):
    tool_calls: list[str]
    text: list[str]
    finished: bool
    errors: list[str]


def parse_jsonl(lines: list[str]) -> Trace:
    tools: list[str] = []
    text: list[str] = []
    finished = False
    errors: list[str] = []
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append("invalid JSONL event")
            continue
        event_type = event.get("type")
        part = event.get("part", {})
        if event_type in {"tool", "tool_use"}:
            name = part.get("tool") or part.get("name")
            if isinstance(name, str):
                tools.append(name)
            else:
                errors.append("tool event without tool name")
        elif event_type == "text" and isinstance(part.get("text"), str):
            text.append(part["text"])
        elif event_type == "step_finish":
            finished = True
        elif event_type in {"error", "tool_error"}:
            errors.append(str(part.get("error") or event.get("error") or event_type))
    return Trace(tools, text, finished, errors)


def classify_result(*, exit_code: int, trace: Trace, diff_ok: bool, checks_ok: bool) -> str:
    narrated_verified = any("VERIFIED" in message for message in trace.text)
    if narrated_verified and (not diff_ok or not checks_ok):
        return "false_green"
    if exit_code != 0:
        return "infra_block"
    if trace.errors:
        return "permission_block"
    if not trace.finished:
        return "timeout"
    return "functional_pass" if diff_ok and checks_ok else "scope_violation"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--opencode", default="opencode")
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--message", default="Classify this as Direct and make no edits. Return BLOCKED if required evidence is unavailable.")
    args = parser.parse_args()
    if shutil.which(args.opencode) is None:
        print(json.dumps({"status": "infra_block", "reason": "opencode executable unavailable"}))
        return 2
    command = [args.opencode, "run", "--command", "orchestrate", "--format", "json", args.message]
    completed = subprocess.run(command, cwd=args.fixture, text=True, capture_output=True, check=False, timeout=120)
    trace = parse_jsonl([line for line in completed.stdout.splitlines() if line.strip()])
    result = classify_result(exit_code=completed.returncode, trace=trace, diff_ok=True, checks_ok=True)
    print(json.dumps({"status": result, "exit_code": completed.returncode, "tools": trace.tool_calls, "text": trace.text, "errors": trace.errors}))
    return 0 if result == "functional_pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
