"""Scoring shim — canonical module: `aegis-sdd/packages/domain/policy_guard.py`."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CANON = Path(__file__).resolve().parents[1] / "aegis-sdd" / "packages" / "domain" / "policy_guard.py"
_spec = importlib.util.spec_from_file_location("aegis_sdd_domain_policy_guard", _CANON)
if _spec is None or _spec.loader is None:
    raise ImportError(f"canonical policy_guard missing: {_CANON}")
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)

Decision = _mod.Decision
BATCH_PROHIBITED = _mod.BATCH_PROHIBITED
PV_PROHIBITED = _mod.PV_PROHIBITED
SUPPLY_PROHIBITED = _mod.SUPPLY_PROHIBITED
WRITE_LIKE_PERMISSIONS = _mod.WRITE_LIKE_PERMISSIONS
check_workflow_payload = _mod.check_workflow_payload
check_authorization = _mod.check_authorization
check_authorization_records = _mod.check_authorization_records
check_tool_manifest = _mod.check_tool_manifest
check_model_artifact = _mod.check_model_artifact

__all__ = [
    "Decision",
    "BATCH_PROHIBITED",
    "PV_PROHIBITED",
    "SUPPLY_PROHIBITED",
    "WRITE_LIKE_PERMISSIONS",
    "check_workflow_payload",
    "check_authorization",
    "check_authorization_records",
    "check_tool_manifest",
    "check_model_artifact",
]
