from __future__ import annotations

import os
from pathlib import Path
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from opencode_runtime import private_runtime


@pytest.mark.live_opencode
def test_v2_effective_agent_and_command_registration():
    executable = os.environ.get("OPENCODE_V2_EXECUTABLE")
    fixture = os.environ.get("OPENCODE_V2_FIXTURE")
    if not executable or not fixture:
        pytest.skip("explicit V2 executable and installed fixture unavailable")
    with private_runtime(executable, Path(fixture).resolve()) as (_, _, proof):
        assert proof["instructions_and_permissions"] == "matched"
        assert proof["command"] == "orchestrate"
        assert len(proof["agents"]) == 4
