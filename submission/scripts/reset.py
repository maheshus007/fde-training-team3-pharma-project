#!/usr/bin/env python3
"""Reset regenerable evaluation evidence outputs (does not touch package evaluation/)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "submission"

REGENERABLE = [
    SUBMISSION / "evidence" / "evaluation_results.json",
]


def main() -> int:
    removed = []
    for p in REGENERABLE:
        if p.exists():
            p.unlink()
            removed.append(p.relative_to(ROOT).as_posix())
    print("reset complete")
    for r in removed:
        print("- removed", r)
    print("re-run: python submission/scripts/evaluate.py")
    print("package evaluation/ untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
