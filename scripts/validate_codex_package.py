"""Static validation for the distributable Codex orchestration package."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

PACKAGE_RELATIVE = Path("packages/codex/skills/codex-orchestrator")
REQUIRED_TERMS = (
    "Direct",
    "Standard",
    "long-running",
    "high-risk",
    "VERIFIED",
    "VERIFIED_WITH_RISKS",
    "FAILED",
    "BLOCKED",
)
LEGACY_ROUTE_TERMS = ("atomic", "normal", "complex")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
LOCAL_PATH = re.compile(r"(?:^|\s)(?:/home/[^\s`]+|/Users/[^\s`]+|[A-Za-z]:\\Users\\[^\s`]+)")
REFERENCE = re.compile(r"(?:\.\.?/|references/)[\w.-]+(?:/[\w.-]+)*\.md\b")


def package_root(root: Path) -> Path:
    return root / PACKAGE_RELATIVE


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
        return ""


def parse_frontmatter(content: str, path: Path, errors: list[str]) -> dict[str, Any]:
    if not content.startswith("---\n"):
        errors.append(f"frontmatter missing at start of {path}")
        return {}

    match = re.search(r"\n---\n", content[4:])
    if match is None:
        errors.append(f"frontmatter closing delimiter missing in {path}")
        return {}

    raw = content[4 : match.start() + 4]
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        errors.append(f"frontmatter invalid in {path}: {exc}")
        return {}

    if not isinstance(parsed, dict):
        errors.append(f"frontmatter must be a mapping in {path}")
        return {}
    return parsed


def validate_frontmatter(skill_path: Path, content: str, errors: list[str]) -> None:
    frontmatter = parse_frontmatter(content, skill_path, errors)
    for key in ("name", "description", "license"):
        if not isinstance(frontmatter.get(key), str) or not frontmatter[key].strip():
            errors.append(f"frontmatter {key!r} missing or invalid in {skill_path}")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("version"), str):
        errors.append(f"frontmatter metadata.version missing or invalid in {skill_path}")
    elif not SEMVER.fullmatch(metadata["version"]):
        errors.append(f"frontmatter metadata.version must be semver in {skill_path}")


def validate_metadata(path: Path, errors: list[str]) -> None:
    content = read_text(path, errors)
    try:
        parsed = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        errors.append(f"metadata YAML invalid in {path}: {exc}")
        return

    if not isinstance(parsed, dict):
        errors.append(f"metadata must be a mapping in {path}")
        return
    policy = parsed.get("policy")
    if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not False:
        errors.append(f"allow_implicit_invocation must be false in {path}")


def validate_model_policy(path: Path, errors: list[str]) -> None:
    content = read_text(path, errors)
    try:
        policy = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        errors.append(f"model routing YAML invalid in {path}: {exc}")
        return
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        errors.append(f"model routing schema_version must be 1 in {path}")
        return
    models = policy.get("models")
    if not isinstance(models, dict):
        errors.append(f"model routing models must be a mapping in {path}")
        return
    expected_roles = {
        "sol": "root-orchestration",
        "terra": "standard-engineering",
        "luna": "mechanical-checked-work",
    }
    for model, expected_role in expected_roles.items():
        config = models.get(model)
        if not isinstance(config, dict):
            errors.append(f"model routing entry missing for {model}")
            continue
        if model == "sol" and config.get("default_effort") != "medium":
            errors.append("Sol default_effort must be medium")
        elif model != "sol" and config.get("default_effort") not in {"medium", "high"}:
            errors.append(f"{model} default_effort must be medium or high")
        if config.get("max_effort") != "high":
            errors.append(f"{model.capitalize()} max_effort must be high")
        if config.get("default_role") != expected_role:
            errors.append(f"{model} default_role must be {expected_role}")


def validate_references(root: Path, path: Path, content: str, errors: list[str]) -> None:
    for match in re.finditer(REFERENCE.pattern, content):
        reference = match.group(0).strip()
        resolved = (path.parent / reference).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"local markdown reference escapes repository in {path}: {reference}")
            continue
        if not resolved.is_file():
            errors.append(f"missing local markdown reference in {path}: {reference}")


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    package = package_root(root)
    skill_path = package / "SKILL.md"
    metadata_path = package / "agents/openai.yaml"
    model_policy_path = package / "references/model-routing.yaml"

    required_references = (
        "index.md",
        "direct.md",
        "standard.md",
        "evidence.md",
        "model-routing.md",
        "long-running.md",
        "high-risk.md",
    )
    for required in (skill_path, metadata_path, model_policy_path, *(package / "references" / name for name in required_references)):
        if not required.is_file():
            errors.append(f"required package file missing: {required}")

    skill_content = read_text(skill_path, errors)
    validate_frontmatter(skill_path, skill_content, errors)
    validate_metadata(metadata_path, errors)
    validate_model_policy(model_policy_path, errors)

    markdown_files = sorted(package.rglob("*.md"))
    combined = "\n".join(read_text(path, errors) for path in markdown_files)
    for path in markdown_files:
        content = read_text(path, errors)
        validate_references(package, path, content, errors)
        if LOCAL_PATH.search(content):
            errors.append(f"machine-local path found in {path}")
        if "[SKILL_PRUNED]" in content or "TODO" in content:
            errors.append(f"unresolved placeholder found in {path}")

    for term in REQUIRED_TERMS:
        if term not in combined:
            errors.append(f"required term missing from Codex references: {term}")

    for term in LEGACY_ROUTE_TERMS:
        pattern = rf"(?:\b{re.escape(term)}\s+route\b|\broute\s+{re.escape(term)}\b)"
        if re.search(pattern, combined, flags=re.IGNORECASE):
            errors.append(f"legacy route term found in package: {term}")

    return errors


def main() -> int:
    root = Path.cwd()
    errors = validate_package(root)
    if errors:
        print("Codex package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Codex package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
