"""Deterministic conflict ranking + advisory note merge. LLM text is never SoT."""
from __future__ import annotations

from typing import Any

# Lower number = review first. Ranking is rules-only (not the model).
_KIND_RANK: dict[str, tuple[int, str]] = {
    "oos_status": (1, "P1 — lab / OOS status disagreement"),
    "genealogy": (1, "P1 — batch genealogy mismatch"),
    "idmp": (1, "P1 — product identity not the same"),
    "logger_pallet": (1, "P1 — logger-pallet association unresolved"),
    "clock": (1, "P1 — receipt clock disagreement"),
    "listedness": (2, "P2 — listedness sources disagree"),
}
_DEFAULT_RANK = (3, "P3 — human review required")


def rank_kind(kind: str) -> tuple[int, str]:
    return _KIND_RANK.get(str(kind or ""), _DEFAULT_RANK)


def template_note(item: dict[str, Any]) -> str:
    kind = str(item.get("kind") or "conflict")
    left = item.get("left") or {}
    right = item.get("right") or {}
    return (
        f"Advisory note ({kind}): {left.get('source') or 'left'} records "
        f"{left.get('verbatim')!r} vs {right.get('source') or 'right'} records "
        f"{right.get('verbatim')!r}. Review both sources before any human decision. "
        "This note does not change evidence and is not a disposition."
    )


def notes_payload(pack: dict[str, Any]) -> dict[str, Any]:
    conflicts = []
    for item in pack.get("contradictions") or []:
        conflicts.append(
            {
                "id": item.get("id"),
                "kind": item.get("kind"),
                "priority": item.get("priority"),
                "priority_label": item.get("priority_label"),
                "left": item.get("left"),
                "right": item.get("right"),
            }
        )
    return {
        "instruction": (
            "Write one short advisory note per conflict. Use only provided verbatim facts. "
            "Do not invent values, units, or identities. Do not recommend release, reject, "
            "allocate, reserve, ship, or reportability."
        ),
        "conflicts": conflicts[:20],
    }


def stub_notes(payload: dict[str, Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in payload.get("conflicts") or []:
        cid = str(item.get("id") or "")
        if not cid:
            continue
        out.append({"id": cid, "note": template_note(item)})
    return out


def extract_notes(suggestions: list[Any] | None) -> dict[str, str]:
    notes: dict[str, str] = {}
    for item in suggestions or []:
        rows: list[Any]
        if isinstance(item, dict) and isinstance(item.get("notes"), list):
            rows = item["notes"]
        elif isinstance(item, list):
            rows = item
        else:
            rows = [item]
        for row in rows:
            if not isinstance(row, dict):
                continue
            cid = str(row.get("id") or "")
            note = str(row.get("note") or "").strip()
            if cid and note:
                notes[cid] = note
    return notes


def prioritize_conflicts(pack: dict[str, Any]) -> dict[str, Any]:
    items = list(pack.get("contradictions") or [])
    ranked: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        updated = dict(item)
        priority, label = rank_kind(str(updated.get("kind") or ""))
        updated["priority"] = priority
        updated["priority_label"] = label
        ranked.append(updated)
    ranked.sort(key=lambda row: (int(row.get("priority") or 99), str(row.get("id") or "")))
    pack["contradictions"] = ranked
    return pack


def merge_advisory_notes(
    pack: dict[str, Any],
    suggestions: list[Any] | None,
    *,
    used: bool,
) -> dict[str, Any]:
    by_id = extract_notes(suggestions)
    source = "azure" if used and by_id else "rules"
    items = []
    for item in pack.get("contradictions") or []:
        if not isinstance(item, dict):
            continue
        updated = dict(item)
        cid = str(updated.get("id") or "")
        updated["advisory_note"] = by_id.get(cid) or template_note(updated)
        updated["note_source"] = source if cid in by_id and used else "rules"
        items.append(updated)
    pack["contradictions"] = items
    return pack
