#!/usr/bin/env python3
"""Delete runtime idempotency/checkpoint/audit JSON only. Never touch challenge data/."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESET_SUBDIRS = ("idempotency", "checkpoints", "audit", "packs")
KEEP_NAMES = {".gitkeep", ".gitignore"}


def evidence_root() -> Path:
    override = str(os.environ.get("AEGIS_EVIDENCE_ROOT") or "").strip()
    if override:
        return Path(override)
    return ROOT / "evidence"


def reset_runtime_stores(root: Path | None = None) -> int:
    base = root or evidence_root()
    deleted = 0
    for name in RESET_SUBDIRS:
        folder = base / name
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if path.is_file() and path.name not in KEEP_NAMES and path.suffix.lower() == ".json":
                path.unlink()
                deleted += 1
    return deleted


def main() -> int:
    deleted = reset_runtime_stores()
    print(f"reset deleted {deleted} runtime json files under {evidence_root()}")
    print("preserved: test_results.json, PREFLIGHT, gitkeep, challenge data/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
