"""Assessment / kill-switch inference stub. No openai import. ≤50 ms."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_DOMAIN = Path(__file__).resolve().parents[2] / "packages" / "domain"
if str(_DOMAIN) not in sys.path:
    sys.path.insert(0, str(_DOMAIN))

_ALLOWED_KINDS = frozenset({"cluster_hint", "option_rank_hint", "narrative_summary", "conflict_notes"})


class InferenceStub:
    def suggest(self, kind: str, payload: dict[str, Any], budget: dict[str, Any] | None = None) -> dict[str, Any]:
        if kind not in _ALLOWED_KINDS:
            return {"used": False, "suggestions": []}
        if kind == "conflict_notes":
            try:
                from conflict_priority import stub_notes
            except Exception:
                return {"used": False, "suggestions": []}
            return {"used": False, "suggestions": stub_notes(payload or {})}
        del payload, budget
        return {"used": False, "suggestions": []}
