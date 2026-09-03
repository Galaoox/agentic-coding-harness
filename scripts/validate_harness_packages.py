"""Static validation for distributable Codex and OpenCode harness packages."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from validate_codex_package import validate_package as validate_codex_package

OPENCODE_RELATIVE = Path("packages/opencode")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
LOCAL_PATH = re.compile(r"(?:^|\s)(?:/home/[^\s`]+|/Users/[^\s`]+|[A-Za-z]:\\Users\\[^\s`]+)")
MARKDOWN_LINK = re.compile(r"\]\(([^)]+\.md)\)")
REQUIRED_TERMS = ("Direct", "Standard", "long-running", "high-risk", "VERIFIED", "VERIFIED_WITH_RISKS", "FAILED", "BLOCKED")
WRITER = "harness-implementer"
READ_ONLY = ("harness-explorer", "harness-verifier")
ALLOWED_WORKERS = {"harness-explorer", "harness-implementer", "harness-verifier"}


def read(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
        return ""


def frontmatter(path: Path, errors: list[str]) -> dict[str, Any]:
    content = read(path, errors)
    if not content.startswith("---\n"):
        errors.append(f"frontmatter missing at start of {path}")
        return {}
    end = content.find("\n---\n", 4)
    if end < 0:
        errors.append(f"frontmatter closing delimiter missing in {path}")
        return {}
    try:
        parsed = yaml.safe_load(content[4:end])
    except yaml.YAMLError as exc:
        errors.append(f"frontmatter invalid in {path}: {exc}")
        return {}
    return parsed if isinstance(parsed, dict) else {}


def action(permission: Any, key: str) -> Any:
    if not isinstance(permission, dict):
        return None
    return permission.get(key)


def validate_opencode_package(root: Path) -> list[str]:
    errors: list[str] = []
    package = root / OPENCODE_RELATIVE
    overlay = package / "overlay/.opencode"
    version = read(package / "VERSION", errors).strip()
    if not SEMVER.fullmatch(version):
        errors.append("OpenCode VERSION must be semver")
    agent_dir = overlay / "agents"
    command = overlay / "commands/orchestrate.md"
    reference_dir = overlay / "references"
    required_references = {
        "index.md",
        "direct.md",
        "standard.md",
        "evidence.md",
        "long-running.md",
        "high-risk.md",
    }
    actual_references = {path.name for path in reference_dir.glob("*.md")}
    if actual_references != required_references:
        errors.append("OpenCode references must contain exactly the modular contract set")
    agent_paths = {path.stem: path for path in agent_dir.glob("*.md")}
    expected = {"harness-orchestrator", *ALLOWED_WORKERS}
    if set(agent_paths) != expected:
        errors.append("OpenCode agent set must contain exactly orchestrator, explorer, implementer, verifier")
    command_data = frontmatter(command, errors)
    if command_data.get("agent") != "harness-orchestrator":
        errors.append("command agent must be harness-orchestrator")
    if command_data.get("subtask") is not False:
        errors.append("command subtask must be false")
    parsed = {name: frontmatter(path, errors) for name, path in agent_paths.items()}
    root_data = parsed.get("harness-orchestrator", {})
    if root_data.get("mode") != "primary":
        errors.append("harness-orchestrator must be primary")
    task = action(root_data.get("permission"), "task")
    if not isinstance(task, dict) or task.get("*") != "deny" or {name for name, value in task.items() if value == "allow"} != ALLOWED_WORKERS:
        errors.append("root task allowlist must allow exactly the three harness workers")
    for name in READ_ONLY:
        data = parsed.get(name, {})
        if data.get("mode") != "subagent" or data.get("hidden") is not True:
            errors.append(f"{name} must be hidden subagent")
        permissions = data.get("permission", {})
        if action(permissions, "edit") != "deny" or action(permissions, "task") != "deny":
            errors.append(f"{name} must deny edit and task")
    explorer = parsed.get("harness-explorer", {}).get("permission", {})
    if action(explorer, "bash") != "deny":
        errors.append("harness-explorer must deny bash")
    implementer = parsed.get(WRITER, {})
    if implementer.get("mode") != "subagent" or action(implementer.get("permission", {}), "edit") != "allow" or action(implementer.get("permission", {}), "task") != "deny":
        errors.append("harness-implementer must be the only writer subagent with task denied")
    reference_content = "\n".join(read(path, errors) for path in sorted(reference_dir.glob("*.md")))
    for term in REQUIRED_TERMS:
        if term not in reference_content:
            errors.append(f"required term missing from OpenCode references: {term}")
    all_files = list(package.rglob("*.md")) + list(package.rglob("*.jsonc"))
    for path in all_files:
        file_content = read(path, errors)
        if LOCAL_PATH.search(file_content):
            errors.append(f"machine-local path found in {path}")
        if "[SKILL_PRUNED]" in file_content or "TODO" in file_content:
            errors.append(f"unresolved placeholder found in {path}")
        if path.is_relative_to(overlay):
            for link in MARKDOWN_LINK.findall(file_content):
                resolved = (path.parent / link).resolve()
                try:
                    resolved.relative_to(overlay.resolve())
                except ValueError:
                    errors.append(f"markdown reference escapes installed overlay in {path}: {link}")
                else:
                    if not resolved.is_file():
                        errors.append(f"missing markdown reference in {path}: {link}")
    if list(package.rglob("openai.yaml")):
        errors.append("Codex metadata openai.yaml is forbidden in OpenCode package")
    return errors


def main() -> int:
    root = Path.cwd()
    errors = validate_codex_package(root) + validate_opencode_package(root)
    try:
        from validate_knowledge_base import validate_knowledge_base
    except ImportError as exc:
        errors.append(f"cannot import knowledge-base validator: {exc}")
    else:
        errors.extend(validate_knowledge_base(root))
    if errors:
        print("Harness package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Harness package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
