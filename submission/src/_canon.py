"""Load canonical aegis-sdd modules without duplicating logic."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

_SUBMISSION = Path(__file__).resolve().parent.parent


def load_canon(module_name: str, relative: str) -> ModuleType:
    path = _SUBMISSION / relative
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"canonical module missing: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod
