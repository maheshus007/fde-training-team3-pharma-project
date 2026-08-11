"""Signed tool manifests (T-012a / INJ-066). Tool text is data, not instructions."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_DOMAIN = Path(__file__).resolve().parent
DEFAULT_APPROVED_HASHES = frozenset({"approvedhash001"})

if str(_DOMAIN) not in sys.path:
    sys.path.insert(0, str(_DOMAIN))

from policy_guard import Decision, check_tool_manifest  # noqa: E402

ALLOWED_TOOL_NAMES = frozenset(
    {
        "resolve_concept",
        "get_provenance",
        "find_conflicts",
        "traverse_evidence_path",
        "assess_readiness",
        "propose_duplicate_candidates",
        "enumerate_draft_options",
        "request_human_review",
        "batch_evidence_read",
    }
)


def load_approved_hashes(path: Path | None = None) -> set[str]:
    if path is None:
        return set(DEFAULT_APPROVED_HASHES)
    doc = json.loads(path.read_text(encoding="utf-8"))
    digest = doc.get("sha256") or doc.get("hash")
    return {str(digest)} if digest else set()


def _instruction_injection(manifest: dict[str, Any]) -> bool:
    chunks = [
        str(manifest.get(key) or "")
        for key in ("description", "instructions", "prompt", "text", "postAction", "post_action")
    ]
    blob = " ".join(chunks).lower()
    if "ignore" in blob and "hold" in blob:
        return True
    if "hidden instruction" in blob:
        return True
    return False


def evaluate_manifest(manifest: dict[str, Any], *, approved_hashes: set[str] | None = None) -> dict[str, Any]:
    """Return allow/deny. Poisoned/unsigned → AEGIS-401 before any tool call."""
    hashes = approved_hashes if approved_hashes is not None else load_approved_hashes()
    if _instruction_injection(manifest):
        decision = Decision(False, "retrieved tool text treated as data; instruction injection denied")
    else:
        decision = check_tool_manifest(manifest, hashes)
        name = str(manifest.get("name") or manifest.get("tool") or "")
        if decision.allow and name and name not in ALLOWED_TOOL_NAMES:
            decision = Decision(False, f"tool name not in approved catalog: {name}")
    if decision.allow:
        return {"allow": True, "reason": decision.reason, "error": None}
    return {
        "allow": False,
        "reason": decision.reason,
        "error": {
            "error": {
                "code": "AEGIS-401",
                "message": decision.reason,
                "request_id": "tool-manifest",
                "retryable": False,
            }
        },
    }
