"""Subgroup / language equity grader — flag low-fidelity languages; require abstention path (INJ-072)."""
from __future__ import annotations

from typing import Any

# Languages with known lower extraction fidelity in package model_performance cues
LOW_FIDELITY_LANGS = frozenset({"ar", "hi", "arabic", "hindi"})


def grade_subgroup(
    payload: dict[str, Any] | None = None,
    *,
    language: str | None = None,
    languages: list[str] | None = None,
) -> dict[str, Any]:
    """Pass when low-fidelity languages are accompanied by abstention or human_review."""
    langs: list[str] = []
    if language:
        langs.append(language)
    if languages:
        langs.extend(languages)
    if isinstance(payload, dict):
        meta = payload.get("subgroup") or payload.get("languages") or []
        if isinstance(meta, list):
            langs.extend(str(x) for x in meta)
        elif isinstance(meta, str):
            langs.append(meta)
        for item in payload.get("evidence") or []:
            if isinstance(item, dict):
                facts = item.get("facts") or {}
                if isinstance(facts, dict) and facts.get("language"):
                    langs.append(str(facts["language"]))

    normalized = [lng.strip().lower() for lng in langs if lng]
    risky = [lng for lng in normalized if lng in LOW_FIDELITY_LANGS]
    if not risky:
        return {
            "grader": "subgroup",
            "result": "pass",
            "gate": "no_low_fidelity_language",
            "detail": "No AR/HI (or equivalent) language markers in payload",
            "languages": normalized,
        }

    abstentions = (payload or {}).get("abstentions") if isinstance(payload, dict) else None
    human = (payload or {}).get("human_review") if isinstance(payload, dict) else None
    has_abstain = isinstance(abstentions, list) and len(abstentions) > 0
    has_human = isinstance(human, dict) and human.get("required") is True
    if has_abstain or has_human:
        return {
            "grader": "subgroup",
            "result": "pass",
            "gate": "low_fidelity_routed",
            "detail": f"Low-fidelity languages {risky} routed via abstention/human_review (INJ-072)",
            "languages": normalized,
        }
    return {
        "grader": "subgroup",
        "result": "fail",
        "gate": "subgroup_uncontrolled",
        "detail": f"Low-fidelity languages {risky} without abstention/human_review",
        "languages": normalized,
    }
