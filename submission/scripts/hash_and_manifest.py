#!/usr/bin/env python3
"""Generate submission/evidence/file_hashes.csv and submission_manifest.csv."""
from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "submission"
EVIDENCE = SUBMISSION / "evidence"
MANIFEST = EVIDENCE / "submission_manifest.csv"

MANIFEST_PREFIXES = (
    "evaluation/",
    "evidence/",
    "scripts/",
    "artefacts/22_",
)


def main() -> int:
    # Prefer package hasher for file_hashes.csv
    rc = subprocess.call([sys.executable, str(ROOT / "tools" / "hash_submission.py")], cwd=str(ROOT))
    if rc != 0:
        return rc

    hashes_path = EVIDENCE / "file_hashes.csv"
    if not hashes_path.exists():
        print("FAIL — file_hashes.csv missing after hash_submission")
        return 1

    with hashes_path.open(encoding="utf-8", newline="") as f:
        hash_rows = list(csv.DictReader(f))

    manifest_rows = []
    for r in hash_rows:
        path = r["path"]
        if not any(path.startswith(p) for p in MANIFEST_PREFIXES):
            continue
        owner = "Team3-Evaluation"
        if path.startswith("artefacts/"):
            owner = "Team3-Artefacts"
        elif path.startswith("scripts/"):
            owner = "Team3-Scripts"
        elif path.startswith("evidence/"):
            owner = "Team3-Evidence"
        manifest_rows.append(
            {
                "path": f"submission/{path}",
                "owner": owner,
                "version": "1.0",
                "status": "active",
                "sha256": r["sha256"],
            }
        )

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "owner", "version", "status", "sha256"])
        w.writeheader()
        w.writerows(manifest_rows)

    # Re-hash so file_hashes includes the new manifest
    rc = subprocess.call([sys.executable, str(ROOT / "tools" / "hash_submission.py")], cwd=str(ROOT))
    print(f"wrote {MANIFEST.relative_to(ROOT)} ({len(manifest_rows)} rows)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
