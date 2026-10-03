"""Deterministic outcome evidence shared by bounded runtime smoke adapters."""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import signal
import shutil
import subprocess

IGNORED = {".git", ".venv", "__pycache__", ".pytest_cache"}
STATES = {"VERIFIED", "VERIFIED_WITH_RISKS", "FAILED", "BLOCKED"}


def snapshot(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    def fail_walk(error: OSError) -> None:
        raise error
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=fail_walk):
        parent = Path(directory)
        links = [name for name in dirs if (parent / name).is_symlink()]
        dirs[:] = sorted(name for name in dirs if name not in IGNORED and name not in links)
        for name in sorted(names + links):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            raw = b"symlink\0" + os.readlink(path).encode() if path.is_symlink() else b"file\0" + path.read_bytes()
            files[relative] = hashlib.sha256(raw).hexdigest()
    return files


def identity(files: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))


def scope_ok(paths: list[str], allowed: list[str]) -> bool:
    return all(any(fnmatch.fnmatchcase(path, pattern) for pattern in allowed) for path in paths)


def output_text(value: str | bytes | None) -> str:
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""


def execute(command: list[str], cwd: Path, timeout: int) -> dict:
    try:
        options = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
        process = subprocess.Popen(command, cwd=cwd, text=True, encoding="utf-8", errors="replace",
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill_process_tree(process)
            stdout, stderr = process.communicate(timeout=5)
            return {"command": command, "cwd": str(cwd), "exit_code": None,
                    "stdout": stdout, "stderr": stderr, "error": "timeout"}
        return {"command": command, "cwd": str(cwd), "exit_code": process.returncode,
                "stdout": stdout, "stderr": stderr, "error": None}
    except subprocess.TimeoutExpired as exc:
        return {"command": command, "cwd": str(cwd), "exit_code": None,
                "stdout": output_text(exc.stdout), "stderr": output_text(exc.stderr), "error": "timeout"}
    except OSError as exc:
        return {"command": command, "cwd": str(cwd), "exit_code": None,
                "stdout": "", "stderr": str(exc), "error": "infra_block"}


def kill_process_tree(process: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=5, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()


def resolve_executable(name: str) -> str | None:
    if os.name != "nt":
        return shutil.which(name)
    # npm supplies both a POSIX shim and a Windows launcher. Never execute the former.
    if PureWindowsPath(name).suffix.lower() in {".exe", ".com", ".cmd", ".bat"}:
        return shutil.which(name)
    for extension in (".exe", ".com", ".cmd", ".bat"):
        resolved = shutil.which(name + extension)
        if resolved:
            return resolved
    return None


def load_case(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("id"), str) or not data["id"]:
        raise ValueError("case requires a non-empty id")
    if not isinstance(data.get("message"), str) or not data["message"]:
        raise ValueError("case requires a message")
    allowed = data.get("allowed_changes")
    if not isinstance(allowed, list) or not all(isinstance(p, str) and p and not p.startswith(("/", "\\"))
                                              and ".." not in p.split("/") and "\\" not in p for p in allowed):
        raise ValueError("allowed_changes must contain repository-relative POSIX patterns")
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks or not all(isinstance(c, list) and c
            and all(isinstance(arg, str) and arg for arg in c) for c in checks):
        raise ValueError("case requires external checks as non-empty argv arrays")
    expected = data.get("expected_terminal")
    if expected is not None and (not isinstance(expected, str) or expected not in STATES):
        raise ValueError("invalid expected_terminal")
    return data


def reported_state(messages: list[str]) -> str | None:
    if not messages:
        return None
    matches = re.findall(r"(?mi)^\s*(?:[#*`]+\s*)?(?:(?:HARNESS_STATE|terminal state|state)\s*[:=]\s*[`*]*)?(VERIFIED_WITH_RISKS|VERIFIED|FAILED|BLOCKED)\b", messages[-1])
    return matches[-1].upper() if matches else None


def verify_case(case: dict, root: Path, timeout: int) -> tuple[list[dict], bool]:
    checks = []
    immutable = True
    for command in case["checks"]:
        before = snapshot(root)
        check = execute(command, root, timeout)
        after = snapshot(root)
        immutable = immutable and before == after
        check["candidate_before"] = identity(before)
        check["candidate_after"] = identity(after)
        checks.append(check)
        if before != after or check["error"]:
            break
    return checks, immutable
