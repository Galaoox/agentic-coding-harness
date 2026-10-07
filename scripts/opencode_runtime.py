"""Own a private V2 server and prove harness registration before model invocation."""
from contextlib import contextmanager
import fnmatch
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import tempfile
import time

import yaml

from smoke_evidence import execute, kill_process_tree

OVERLAY = Path(__file__).resolve().parents[1] / "packages/opencode/overlay/.opencode"


def expected_agents() -> dict:
    result = {}
    for path in (OVERLAY / "agents").glob("*.md"):
        _, header, body = path.read_text(encoding="utf-8").split("---", 2)
        result[path.stem] = dict(yaml.safe_load(header), system=body.strip())
    return result


def check_registration(agents: list, commands: list) -> dict:
    expected = expected_agents()
    actual = {agent["id"]: agent for agent in agents}
    for name, source in expected.items():
        observed = actual.get(name)
        if not observed or observed.get("mode") != source["mode"] or observed.get("hidden"):
            raise ValueError("missing or incompatible agent: " + name)
        if observed.get("system", "").strip().replace("\r\n", "\n") != source["system"]:
            raise ValueError("agent instructions differ: " + name)
        rules = observed.get("permissions", [])
        actions = {rule["action"] for rule in source["permissions"]}
        # Preserve order and reject later broad overrides. Runtime defaults may
        # precede the package rules; builtin browser policy is unrelated.
        relevant = [rule for rule in rules if rule.get("action") in actions]
        if relevant != source["permissions"]:
            raise ValueError("agent permissions differ: " + name)
        block = source["permissions"]
        starts = [i for i in range(len(rules)) if rules[i:i + len(block)] == block]
        if len(starts) != 1:
            raise ValueError("agent permission block differs: " + name)
        for rule in rules[starts[0] + len(block):]:
            if any(fnmatch.fnmatchcase(action, rule["action"]) for action in actions):
                raise ValueError("agent permission overridden: " + name)
    if not any(command.get("name") == "orchestrate" for command in commands):
        raise ValueError("orchestrate command not registered")
    return {"agents": sorted(expected), "command": "orchestrate", "instructions_and_permissions": "matched"}


@contextmanager
def private_runtime(executable: str, root: Path, timeout: int = 30, config_dir: Path | None = None):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    url = "http://127.0.0.1:" + str(port)
    env = dict(os.environ, OPENCODE_PASSWORD=secrets.token_urlsafe(32), PYTHONDONTWRITEBYTECODE="1")
    if config_dir is not None:
        env["OPENCODE_CONFIG_DIR"] = str(config_dir.resolve(strict=True))
    options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW}
               if os.name == "nt" else {"start_new_session": True})
    with tempfile.TemporaryFile() as log:
        server = subprocess.Popen([executable, "serve", "--hostname", "127.0.0.1", "--port", str(port)],
                                  cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=log, **options)
        try:
            deadline = time.monotonic() + timeout
            reason = "server did not become ready"
            while time.monotonic() < deadline and server.poll() is None:
                try:
                    catalogs = []
                    for operation in ("agent.list", "command.list"):
                        remaining = max(1, min(5, int(deadline - time.monotonic())))
                        response = execute([executable, "api", "--server", url, operation,
                                            "--param", "location[directory]=" + str(root)], root, remaining, env=env)
                        if response["exit_code"] != 0 or response["error"]:
                            raise ValueError("catalog request failed: " + operation)
                        catalogs.append(json.loads(response["stdout"])["data"])
                    proof = check_registration(*catalogs)
                    break
                except (ValueError, KeyError, TypeError) as exc:
                    reason = str(exc)
                time.sleep(min(0.2, max(0, deadline - time.monotonic())))
            else:
                raise ValueError("OpenCode registration preflight failed: " + reason)
            yield url, env, proof
        finally:
            try:
                kill_process_tree(server)
                server.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise ValueError("OpenCode private server cleanup failed") from exc
