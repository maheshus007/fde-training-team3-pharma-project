"""Shim — canonical: aegis-sdd/packages/domain/tool_catalog.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_domain_tool_catalog",
    "aegis-sdd/packages/domain/tool_catalog.py",
)
evaluate_manifest = _mod.evaluate_manifest
load_approved_hashes = _mod.load_approved_hashes
ALLOWED_TOOL_NAMES = _mod.ALLOWED_TOOL_NAMES
