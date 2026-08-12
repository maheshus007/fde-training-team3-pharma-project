#!/usr/bin/env python3
"""Validate local layout for evaluation / offline deterministic runs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "submission"

REQUIRED = [
    SUBMISSION / "evaluation" / "TEVV_PLAN.md",
    SUBMISSION / "evaluation" / "datasets" / "thresholds.json",
    SUBMISSION / "evaluation" / "graders" / "test_graders.py",
    ROOT / "evaluation" / "PUBLIC_FIXTURE_INDEX.csv",
    ROOT / "evaluation" / "contracts",
]


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
    if missing:
        print("FAIL — setup prerequisites missing:")
        for m in missing:
            print("-", m)
        return 1
    print("PASS — evaluation setup prerequisites present")
    print("runtime_mode_default: ai_disabled_deterministic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
