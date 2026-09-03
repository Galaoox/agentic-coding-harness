from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.live_opencode
def test_capability_spike_command_and_agent_are_discovered() -> None:
    fixture = Path(os.environ.get("OPENCODE_CAPABILITY_FIXTURE", "/tmp/opencode-capability"))
    if not fixture.is_dir():
        pytest.skip("capability fixture unavailable")
    result = subprocess.run(
        ["opencode", "debug", "config"],
        cwd=fixture,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert '"cap-primary"' in result.stdout
    assert '"capability"' in result.stdout
