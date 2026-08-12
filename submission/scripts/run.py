#!/usr/bin/env python3
"""Start advisory POC UI (optional). Evaluation itself uses evaluate.py offline."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "submission" / "app" / "taipy_app.py"


def main() -> int:
    if not APP.exists():
        print(f"FAIL — missing {APP.relative_to(ROOT)}")
        return 1
    print("Starting Taipy advisory UI (AI-disabled path available in app).")
    print("For gates use: python submission/scripts/evaluate.py")
    return subprocess.call([sys.executable, str(APP)], cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
