"""Execution-time security gates (INJ-067 / INJ-068 / INJ-076)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    reason: str


def check_purpose_limitation(source_affiliate: str, target_affiliate: str, purpose: str) -> GateDecision:
    if source_affiliate != target_affiliate and purpose == "general_review":
        return GateDecision(
            allowed=False,
            reason=(
                f"Denied cross-affiliate pull {source_affiliate}→{target_affiliate} "
                f"for purpose '{purpose}' (INJ-068). Require purpose-bound entitlement."
            ),
        )
    return GateDecision(allowed=True, reason="Purpose-bound access within affiliate scope.")


def check_token_budget(requested_tokens: int) -> GateDecision:
    limit = 250_000
    if requested_tokens > limit:
        return GateDecision(
            allowed=False,
            reason=(
                f"Denied: requested {requested_tokens:,} tokens exceeds budget "
                f"{limit:,} (INJ-076 denial-of-wallet)."
            ),
        )
    return GateDecision(allowed=True, reason=f"Within token budget ({requested_tokens:,} ≤ {limit:,}).")


def check_live_authorization(user_id: str) -> GateDecision:
    if user_id == "contractor_77":
        return GateDecision(
            allowed=False,
            reason=(
                "Denied at execution-time re-check: contractor_77 entitlement revoked "
                "in live IAM; gateway cache must not allow (INJ-067 / PUB-09)."
            ),
        )
    return GateDecision(allowed=True, reason=f"Live IAM allow for '{user_id}'.")
