"""Shim — canonical: aegis-sdd/services/integration/entitlements.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_entitlements",
    "aegis-sdd/services/integration/entitlements.py",
)
EntitlementStore = _mod.EntitlementStore
AuthzResult = _mod.AuthzResult
ALLOWED_PURPOSES = _mod.ALLOWED_PURPOSES
WORKFLOW_PURPOSE = _mod.WORKFLOW_PURPOSE
