"""Stale entitlement cache must deny at execution time (INJ-067)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT))

from src.policy_guard import (  # noqa: E402
    check_authorization,
    check_authorization_records,
)


class AuthorizationFreshnessTests(unittest.TestCase):
    def test_stale_cache_denied(self) -> None:
        d = check_authorization(
            entitlement_active=True,
            cache_says_allow=True,
            cache_fresh=False,
        )
        self.assertFalse(d.allow)
        self.assertIn("stale", d.reason)

    def test_revoked_denied_even_if_cache_allows(self) -> None:
        d = check_authorization(
            entitlement_active=False,
            cache_says_allow=True,
            cache_fresh=True,
        )
        self.assertFalse(d.allow)

    def test_fresh_allow(self) -> None:
        d = check_authorization(
            entitlement_active=True,
            cache_says_allow=True,
            cache_fresh=True,
        )
        self.assertTrue(d.allow)

    def test_fixture_contractor_stale_cache_denied(self) -> None:
        entitlements = json.loads((FIX / "users_entitlements.json").read_text(encoding="utf-8"))
        cache = json.loads((FIX / "access_cache_stale.json").read_text(encoding="utf-8"))
        d = check_authorization_records(
            entitlements["contractor_77"],
            cache,
            as_of="2026-08-02T12:00:00Z",
        )
        self.assertFalse(d.allow)

    def test_fixture_active_qp_allowed(self) -> None:
        entitlements = json.loads((FIX / "users_entitlements.json").read_text(encoding="utf-8"))
        d = check_authorization_records(
            entitlements["qp_eu_1"],
            {"user": "qp_eu_1", "cached_until": "2026-08-10T00:00:00Z", "gateway_state": "active"},
            as_of="2026-08-02T12:00:00Z",
        )
        self.assertTrue(d.allow)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
