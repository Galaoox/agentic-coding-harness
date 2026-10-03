"""Report deterministic context sizes for declared harness scenarios."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

CATALOG = Path("docs/knowledge-base.yaml")


def measure_files(paths: list[Path]) -> dict[str, int]:
    metrics = {"bytes": 0, "raw_bytes": 0, "characters": 0, "lines": 0, "words": 0}
    for path in paths:
        raw = path.read_bytes()
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        metrics["raw_bytes"] += len(raw)
        metrics["bytes"] += len(text.encode("utf-8"))
        metrics["characters"] += len(text)
        metrics["lines"] += len(text.splitlines())
        metrics["words"] += len(text.split())
    return metrics


def measure_layers(path: Path) -> list[dict[str, Any]]:
    """Explicit per-role inputs; never discover private global configuration implicitly."""
    layers = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(layers, list):
        raise ValueError("layers must be an array of role/layer/files objects")
    result = []
    for entry in layers:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) for key in ("role", "layer")):
            raise ValueError("each layer requires role and layer strings")
        paths = entry.get("files")
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths):
            raise ValueError("each layer requires non-empty files")
        sources = [Path(p) if Path(p).is_absolute() else path.parent / p for p in paths]
        result.append({**entry, **measure_files(sources)})
    return result


def build_report(root: Path) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load((root / CATALOG).read_text(encoding="utf-8"))
    report: dict[str, dict[str, Any]] = {}
    for name, spec in sorted(data["context_scenarios"].items()):
        always = list(spec["always"])
        conditional = list(spec["conditional"])
        files = always + conditional
        max_bytes = int(spec["max_bytes"])
        metrics = measure_files([root / relative for relative in files])
        report[name] = {
            "files": files,
            "always": always,
            "conditional": conditional,
            **metrics,
            "measurement": "declared package files, LF-normalized; not model tokens",
            "max_bytes": max_bytes,
            "within_budget": metrics["bytes"] <= max_bytes,
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--layers", type=Path, help="explicit observed context layers, grouped by role")
    parser.add_argument("--run-result", type=Path, help="smoke result with measured runtime usage")
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    observations = {}
    if args.layers:
        observations["layers"] = measure_layers(args.layers)
    if args.run_result:
        result = json.loads(args.run_result.read_text(encoding="utf-8"))
        observations["run"] = {key: result.get(key) for key in ("runtime", "model", "effort", "evaluation", "metrics")}
    if args.json:
        print(json.dumps({"scenarios": report, "observations": observations} if observations else report, indent=2, sort_keys=True))
        return 0 if all(s["within_budget"] for s in report.values()) else 1
    print("scenario\tfiles\tbytes_lf\tmax_bytes\twithin_budget\traw_bytes\tlines\twords")
    for name, metrics in report.items():
        print(f"{name}\t{len(metrics['files'])}\t{metrics['bytes']}\t{metrics['max_bytes']}\t{metrics['within_budget']}\t{metrics['raw_bytes']}\t{metrics['lines']}\t{metrics['words']}")
    if observations:
        print(json.dumps(observations, indent=2))
    return 0 if all(s["within_budget"] for s in report.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
