#!/usr/bin/env python3
"""Assessment setup: stdlib only, no Azure/Cosmos keys required (AA-NFR-09/16)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("AEGIS_RUNTIME_MODE", "assessment")
os.environ.setdefault("AEGIS_GRAPH_FALLBACK", "true")

EXAMPLE = ROOT / "aegis-sdd" / ".env.example"
print("AEGIS assessment setup")
print("runtime mode:", os.environ["AEGIS_RUNTIME_MODE"])
print("python:", sys.version.split()[0])
print("env template:", EXAMPLE if EXAMPLE.is_file() else "missing")
print("do not commit secrets; leave Azure and Cosmos vars unset for CI")
print("next: python submission/scripts/test.py")
raise SystemExit(0)
