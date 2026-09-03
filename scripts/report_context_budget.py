"""Report deterministic context sizes for declared harness scenarios."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

CATALOG = Path("docs/knowledge-base.yaml")


def build_report(root: Path) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load((root / CATALOG).read_text(encoding="utf-8"))
    report: dict[str, dict[str, Any]] = {}
    for name, spec in sorted(data["context_scenarios"].items()):
        always = list(spec["always"])
        conditional = list(spec["conditional"])
        files = always + conditional
        max_bytes = int(spec["max_bytes"])
        byte_count = char_count = line_count = word_count = 0
        for relative in files:
            raw = (root / relative).read_bytes()
            text = raw.decode("utf-8")
            byte_count += len(raw)
            char_count += len(text)
            line_count += len(text.splitlines())
            word_count += len(text.split())
        report[name] = {
            "files": files,
            "always": always,
            "conditional": conditional,
            "bytes": byte_count,
            "characters": char_count,
            "lines": line_count,
            "words": word_count,
            "max_bytes": max_bytes,
            "within_budget": byte_count <= max_bytes,
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    print("scenario\tfiles\tbytes\tmax_bytes\twithin_budget\tcharacters\tlines\twords")
    for name, metrics in report.items():
        print(f"{name}\t{len(metrics['files'])}\t{metrics['bytes']}\t{metrics['max_bytes']}\t{metrics['within_budget']}\t{metrics['characters']}\t{metrics['lines']}\t{metrics['words']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
