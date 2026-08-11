#!/usr/bin/env python3
"""Run assessment service: health + fixture ingest. Does not launch Taipy."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("AEGIS_RUNTIME_MODE", "assessment")

from src.service import health, ingest_graph  # noqa: E402

print(json.dumps(health(), sort_keys=True))
print(json.dumps(ingest_graph(), sort_keys=True))
print("HITL UI (optional, needs Taipy): python submission/app/main.py  # binds 127.0.0.1")
raise SystemExit(0)
