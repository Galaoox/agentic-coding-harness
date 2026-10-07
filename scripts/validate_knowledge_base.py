"""Validate the repository knowledge map and progressive context declarations."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

CATALOG = Path("docs/knowledge-base.yaml")
LINK = re.compile(r"\[[^]]*\]\(([^)#?]+)(?:#[^)]+)?\)")
AUTHORITIES = {"normative", "evidence", "historical", "reference"}
STATUSES = {"current", "completed", "superseded"}
RUNTIMES = {"codex", "opencode"}
RUNTIME_SUPPORT_MARKER = "<!-- supported-runtimes: codex, opencode -->"
MACHINE_LOCAL_PATH = re.compile(r"(?:^|\s)(?:/home/[^\s`]+|/Users/[^\s`]+|[A-Za-z]:\\Users\\[^\s`]+)")
UNRESOLVED_PLACEHOLDERS = ("[SKILL_PRUNED]", "TODO", "TBD")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
REQUIRED_SCENARIOS = {
    "repository-bootstrap",
    "codex-direct",
    "codex-direct-long-running",
    "codex-standard",
    "codex-standard-long-running",
    "codex-standard-high-risk",
    "opencode-direct",
    "opencode-direct-long-running",
    "opencode-standard",
    "opencode-standard-long-running",
    "opencode-standard-high-risk",
}


def read_yaml(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"cannot read knowledge catalog: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append("knowledge catalog must be a mapping")
        return {}
    return value


def validate_links(root: Path, paths: list[Path], errors: list[str]) -> None:
    resolved_root = root.resolve()
    for path in paths:
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"cannot read {path}: {exc}")
            continue
        for target in LINK.findall(content):
            if URI_SCHEME.match(target) or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(resolved_root)
            except ValueError:
                errors.append(f"local link escapes repository in {path.relative_to(root)}: {target}")
            else:
                if not resolved.exists():
                    errors.append(f"broken local link in {path.relative_to(root)}: {target}")


def validate_package_boundary(root: Path, package: Path, errors: list[str]) -> None:
    for path in package.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for target in LINK.findall(content):
            if URI_SCHEME.match(target) or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(package.resolve())
            except ValueError:
                errors.append(f"runtime reference escapes installed package in {path.relative_to(root)}: {target}")
            else:
                if not resolved.exists():
                    errors.append(f"broken runtime package link in {path.relative_to(root)}: {target}")


def validate_knowledge_base(root: Path) -> list[str]:
    errors: list[str] = []
    data = read_yaml(root / CATALOG, errors)
    if not data:
        return errors
    if data.get("schema_version") != 1:
        errors.append("knowledge catalog schema_version must be 1")
    runtimes = data.get("supported_runtimes")
    if not isinstance(runtimes, list) or not all(isinstance(value, str) for value in runtimes) or set(runtimes) != RUNTIMES:
        errors.append("supported_runtimes must contain exactly codex and opencode")

    runtime_versions = data.get("runtime_versions")
    if not isinstance(runtime_versions, dict) or not all(isinstance(key, str) for key in runtime_versions) or set(runtime_versions) != RUNTIMES:
        errors.append("runtime_versions must contain exactly codex and opencode")
        runtime_versions = {}
    codex_skill = root / "packages/codex/skills/codex-orchestrator/SKILL.md"
    codex_version = ""
    if codex_skill.is_file():
        parts = codex_skill.read_text(encoding="utf-8").split("---", 2)
        if len(parts) == 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
            except yaml.YAMLError as exc:
                errors.append(f"cannot read Codex runtime version: {exc}")
            else:
                if isinstance(frontmatter, dict) and isinstance(frontmatter.get("metadata"), dict):
                    codex_version = str(frontmatter["metadata"].get("version", ""))
    opencode_version_path = root / "packages/opencode/VERSION"
    opencode_version = opencode_version_path.read_text(encoding="utf-8").strip() if opencode_version_path.is_file() else ""
    actual_versions = {"codex": codex_version, "opencode": opencode_version}
    for runtime, actual in actual_versions.items():
        if runtime_versions.get(runtime) != actual:
            errors.append(f"runtime version drift for {runtime}: catalog={runtime_versions.get(runtime)!r}, package={actual!r}")

    capabilities = data.get("adapter_conformance", {})
    expected_capabilities = {"causal-corrections", "direct-reclassification", "continuity", "planning-handoffs", "reproduction-verification", "premise-browser"}
    if not isinstance(capabilities, dict) or set(capabilities) != expected_capabilities:
        errors.append("adapter_conformance must declare the six shared capabilities")
    else:
        for name, spec in capabilities.items():
            if not isinstance(spec, dict) or any(spec.get(runtime) != "specified" for runtime in RUNTIMES) or spec.get("behavioral_evidence") != "pending":
                errors.append(f"invalid or unsupported conformance claim: {name}")

    documents = data.get("documents")
    if not isinstance(documents, list):
        errors.append("documents must be a list")
        documents = []
    seen: set[str] = set()
    catalogued_paths: list[Path] = []
    for item in documents:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            errors.append("each document entry must have a string path")
            continue
        relative = item["path"]
        if relative in seen:
            errors.append(f"duplicate document path: {relative}")
        seen.add(relative)
        path = (root / relative).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"catalogued path escapes repository: {relative}")
            continue
        catalogued_paths.append(path)
        if not path.is_file():
            errors.append(f"catalogued document missing: {relative}")
        if item.get("authority") not in AUTHORITIES:
            errors.append(f"invalid authority for {relative}")
        if item.get("status") not in STATUSES:
            errors.append(f"invalid status for {relative}")
        if not isinstance(item.get("scope"), str) or not item["scope"]:
            errors.append(f"invalid scope for {relative}")

    required_normative = {
        "docs/index.md",
        "docs/architecture.md",
        "packages/core/contracts/evidence-driven-orchestration.md",
        "packages/core/principles/memory-authority.md",
    }
    for directory in (root / "docs/contracts", root / "docs/runtimes"):
        required_normative.update(path.relative_to(root).as_posix() for path in directory.glob("*.md"))
    missing = sorted(required_normative - seen)
    for relative in missing:
        errors.append(f"normative document is not catalogued: {relative}")
    knowledge_documents = {path.relative_to(root).as_posix() for path in (root / "docs").rglob("*.md")}
    for relative in sorted(knowledge_documents - seen):
        errors.append(f"knowledge document is not catalogued: {relative}")

    scenarios = data.get("context_scenarios")
    if not isinstance(scenarios, dict):
        errors.append("context_scenarios must be a mapping")
        scenarios = {}
    if not all(isinstance(name, str) for name in scenarios):
        errors.append("context scenario names must be strings")
    elif set(scenarios) != REQUIRED_SCENARIOS:
        errors.append("context scenarios do not match the required set")
    for name, spec in scenarios.items():
        if not isinstance(name, str):
            continue
        always = spec.get("always") if isinstance(spec, dict) else None
        conditional = spec.get("conditional") if isinstance(spec, dict) else None
        max_bytes = spec.get("max_bytes") if isinstance(spec, dict) else None
        if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes <= 0:
            errors.append(f"context scenario {name} must declare positive max_bytes")
        if not isinstance(always, list) or not always:
            errors.append(f"context scenario {name} must declare non-empty always files")
            continue
        if not isinstance(conditional, list):
            errors.append(f"context scenario {name} must declare conditional files")
            continue
        files = always + conditional
        if not all(isinstance(relative, str) for relative in files):
            errors.append(f"context scenario {name} file entries must be strings")
            continue
        if len(files) != len(set(files)):
            errors.append(f"context scenario {name} contains duplicate files")
        existing_context_files: list[Path] = []
        for relative in files:
            if not isinstance(relative, str):
                errors.append(f"context scenario {name} references missing file: {relative}")
                continue
            context_path = (root / relative).resolve()
            try:
                context_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"context path escapes repository in {name}: {relative}")
                continue
            if not context_path.is_file():
                errors.append(f"context scenario {name} references missing file: {relative}")
            else:
                existing_context_files.append(context_path)
        if isinstance(max_bytes, int) and not isinstance(max_bytes, bool) and max_bytes > 0:
            byte_count = sum(len(path.read_text(encoding="utf-8").encode("utf-8")) for path in existing_context_files)
            if byte_count > max_bytes:
                errors.append(f"context scenario {name} exceeds max_bytes: {byte_count} > {max_bytes}")
        joined = "\n".join(str(value) for value in files)
        if name.endswith("-direct") and any(term in joined for term in ("standard.md", "long-running.md", "high-risk.md")):
            errors.append(f"Direct context scenario loads unrelated contract: {name}")
        if name in {"codex-standard", "opencode-standard"} and any(term in joined for term in ("long-running.md", "high-risk.md")):
            errors.append(f"Standard context scenario preloads modifier: {name}")

    agents = (root / "AGENTS.md").read_text(encoding="utf-8") if (root / "AGENTS.md").is_file() else ""
    if len(agents.splitlines()) >= 100:
        errors.append("AGENTS.md must remain below 100 lines")
    if "docs/index.md" not in agents or "Codex" not in agents or "OpenCode" not in agents:
        errors.append("AGENTS.md must map the knowledge base and supported runtimes")
    if "Codex is the only supported runtime" in agents:
        errors.append("AGENTS.md contains stale Codex-only support")

    for relative in ("AGENTS.md", "README.md", "docs/architecture.md"):
        path = root / relative
        content = path.read_text(encoding="utf-8") if path.is_file() else ""
        if RUNTIME_SUPPORT_MARKER not in content:
            errors.append(f"runtime support marker missing or stale in {relative}")
    for relative in ("README.md", "docs/architecture.md"):
        path = root / relative
        content = path.read_text(encoding="utf-8") if path.is_file() else ""
        for runtime, label in (("codex", "Codex"), ("opencode", "OpenCode")):
            version = actual_versions[runtime]
            display_version = version.rsplit(".", 1)[0] if version.count(".") == 2 else version
            markers = (f"{label} v{display_version}", f"{label} adapter v{display_version}")
            if version and not any(marker in content for marker in markers):
                errors.append(f"runtime version marker missing or stale for {runtime} in {relative}")

    model_policy = root / "packages/codex/skills/codex-orchestrator/references/model-routing.md"
    if model_policy.is_file():
        policy = model_policy.read_text(encoding="utf-8")
        if "Sol `high` is the hard ceiling" not in policy:
            errors.append("Codex model policy must cap Sol at high")

    existing = [path for path in catalogued_paths if path.is_file()]
    existing.extend([root / "AGENTS.md", root / "README.md"])
    for path in existing:
        content = path.read_text(encoding="utf-8")
        if MACHINE_LOCAL_PATH.search(content):
            errors.append(f"machine-local path found in {path.relative_to(root)}")
        if any(marker in content for marker in UNRESOLVED_PLACEHOLDERS):
            errors.append(f"unresolved placeholder found in {path.relative_to(root)}")
    validate_links(root, existing, errors)
    validate_package_boundary(root, root / "packages/codex/skills/codex-orchestrator", errors)
    validate_package_boundary(root, root / "packages/opencode/overlay/.opencode", errors)
    return errors


def main() -> int:
    root = Path.cwd()
    errors = validate_knowledge_base(root)
    if errors:
        print("Knowledge base validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Knowledge base validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
