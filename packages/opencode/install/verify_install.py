"""Verify a project-scoped OpenCode overlay without writing it."""
from __future__ import annotations

import argparse
from pathlib import Path

from install import verify_install


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    args = parser.parse_args()
    errors = verify_install(args.target)
    if errors:
        print("OpenCode overlay verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OpenCode overlay verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
