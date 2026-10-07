import copy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from opencode_runtime import check_registration, expected_agents
import opencode_runtime


def catalogs():
    agents = [dict(source, id=name, hidden=False) for name, source in expected_agents().items()]
    for agent in agents:
        agent["permissions"] = [{"action": "*", "resource": "*", "effect": "allow"}, *agent["permissions"]]
    return agents, [{"name": "orchestrate"}]


def test_registration_accepts_inherited_defaults_and_native_rules():
    assert check_registration(*catalogs())["instructions_and_permissions"] == "matched"


@pytest.mark.parametrize("defect", ["missing", "hidden", "mode", "instructions", "override", "resource_override", "order", "command"])
def test_registration_rejects_incomplete_or_changed_profiles(defect):
    agents, commands = copy.deepcopy(catalogs())
    root = next(agent for agent in agents if agent["id"] == "harness-orchestrator")
    if defect == "missing":
        agents.remove(root)
    elif defect == "hidden":
        root["hidden"] = True
    elif defect == "mode":
        root["mode"] = "subagent"
    elif defect == "instructions":
        root["system"] = "unrelated agent"
    elif defect == "override":
        root["permissions"].append({"action": "*", "resource": "*", "effect": "allow"})
    elif defect == "resource_override":
        verifier = next(agent for agent in agents if agent["id"] == "harness-verifier")
        verifier["permissions"].append({"action": "*", "resource": "*.py", "effect": "allow"})
    elif defect == "order":
        root["permissions"].reverse()
    elif defect == "command":
        commands.clear()
    with pytest.raises(ValueError):
        check_registration(agents, commands)


def test_registration_timeout_terminates_only_owned_server(tmp_path, monkeypatch):
    class Server:
        def poll(self):
            return None
        def wait(self, timeout):
            return -1
    server, killed = Server(), []
    monkeypatch.setattr(opencode_runtime.subprocess, "Popen", lambda *args, **kwargs: server)
    monkeypatch.setattr(opencode_runtime, "kill_process_tree", lambda process: killed.append(process))
    with pytest.raises(ValueError, match="preflight failed"):
        with opencode_runtime.private_runtime("runtime", tmp_path, timeout=0):
            pytest.fail("must not yield an unregistered server")
    assert killed == [server]
