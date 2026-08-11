"""Execution-time entitlement + purpose re-check (T-004 / INJ-067 / PRI-01).

Canonical product module. Scoring shim: `submission/src/adapters/entitlements.py`.
Azure AD is out of scope; fixtures only.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_DOMAIN = Path(__file__).resolve().parents[2] / "packages" / "domain"
if str(_DOMAIN) not in sys.path:
    sys.path.insert(0, str(_DOMAIN))

from policy_guard import check_authorization_records  # noqa: E402

_SUBMISSION = Path(__file__).resolve().parents[3]
_DEFAULT_ENTITLEMENTS = _SUBMISSION / "tests" / "fixtures" / "users_entitlements.json"
_DEFAULT_STALE_CACHE = _SUBMISSION / "tests" / "fixtures" / "access_cache_stale.json"

ALLOWED_PURPOSES = frozenset({"batch_review_readiness", "pv_intake", "supply_options"})
WORKFLOW_PURPOSE = {
    "batch_evidence": "batch_review_readiness",
    "pv_intake": "pv_intake",
    "supply_options": "supply_options",
}
PURPOSE_OBJECT_CLASS = {
    "batch_review_readiness": "batch",
    "pv_intake": "pv",
    "supply_options": "supply",
}


@dataclass(frozen=True)
class AuthzResult:
    allow: bool
    reason: str
    error: dict[str, Any] | None


def _deny(request_id: str, message: str) -> AuthzResult:
    return AuthzResult(
        allow=False,
        reason=message,
        error={
            "error": {
                "code": "AEGIS-401",
                "message": message,
                "request_id": str(request_id),
                "retryable": False,
            }
        },
    )


def _object_class(object_id: str) -> str | None:
    oid = str(object_id).strip().upper()
    if oid.startswith("PV-"):
        return "pv"
    if oid.startswith("SH-") or oid.startswith("LG-") or oid.startswith("P-"):
        return "supply"
    if oid.startswith("NCB") or "-B" in oid:
        return "batch"
    return None


class EntitlementStore:
    def __init__(
        self,
        entitlements_path: Path | None = None,
        stale_cache_path: Path | None = None,
    ) -> None:
        ent_path = entitlements_path or _DEFAULT_ENTITLEMENTS
        cache_path = stale_cache_path or _DEFAULT_STALE_CACHE
        self._entitlements: dict[str, Any] = json.loads(ent_path.read_text(encoding="utf-8"))
        self._stale_cache: dict[str, Any] = json.loads(cache_path.read_text(encoding="utf-8"))

    def _cache_for(self, user: str) -> Mapping[str, Any]:
        if str(self._stale_cache.get("user", "")) == user:
            return self._stale_cache
        return {
            "user": user,
            "cached_until": "2099-01-01T00:00:00Z",
            "gateway_state": "active",
            "allow": True,
        }

    def authorize(
        self,
        *,
        user: str,
        purpose: str,
        object_id: str,
        role: str,
        workflow: str,
        as_of: str,
        request_id: str,
    ) -> AuthzResult:
        entitlement = self._entitlements.get(user)
        if not isinstance(entitlement, dict):
            return _deny(request_id, "unknown user")

        fresh = check_authorization_records(entitlement, self._cache_for(user), as_of=as_of)
        if not fresh.allow:
            return _deny(request_id, fresh.reason)

        if purpose not in ALLOWED_PURPOSES:
            return _deny(request_id, "purpose mismatch")
        required = WORKFLOW_PURPOSE.get(workflow)
        if required is None or purpose != required:
            return _deny(request_id, "purpose mismatch")

        obj_class = _object_class(object_id)
        expected_class = PURPOSE_OBJECT_CLASS[purpose]
        if obj_class is not None and obj_class != expected_class:
            return _deny(request_id, "purpose mismatch")

        allowed_purposes = entitlement.get("purposes")
        if isinstance(allowed_purposes, list) and purpose not in allowed_purposes:
            return _deny(request_id, "purpose mismatch")

        allowed_objects = entitlement.get("object_ids")
        if isinstance(allowed_objects, list) and object_id not in allowed_objects:
            return _deny(request_id, "purpose mismatch")

        ent_role = str(entitlement.get("role") or "")
        if ent_role and role and role != ent_role:
            return _deny(request_id, "role mismatch")

        return AuthzResult(allow=True, reason="fresh allow", error=None)
