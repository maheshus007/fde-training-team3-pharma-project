#!/usr/bin/env python3
"""Validate / report gaps in EVIDENCE_MAP.md vs package inject catalogues."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EMAP = ROOT / "submission" / "artefacts" / "EVIDENCE_MAP.md"


def resolve_source(token: str) -> tuple[str, bool]:
    tok = token.strip()
    if not tok:
        return tok, False
    candidates = [
        ROOT / "data" / tok,
        ROOT / "knowledge" / tok,
        ROOT / "source_documents" / tok,
        ROOT / "case" / tok,
        ROOT / tok,
    ]
    for c in candidates:
        if c.is_file():
            return c.relative_to(ROOT).as_posix(), True
    # knowledge/ already prefixed in some CSV cells
    if (ROOT / tok).is_file():
        return Path(tok).as_posix(), True
    return tok, False


def main() -> int:
    emap = EMAP.read_text(encoding="utf-8")
    inj = {x["id"]: x for x in json.loads((ROOT / "data" / "injects.json").read_text(encoding="utf-8"))}
    rows = list(csv.DictReader((ROOT / "data" / "inject_evidence_map.csv").open(encoding="utf-8")))
    by_id = {r["inject_id"]: r for r in rows}

    found = set(re.findall(r"INJ-\d{3}", emap))
    missing = sorted(set(inj) - found, key=lambda s: int(s.split("-")[1]))
    print(f"coverage {len(found & set(inj))}/84 missing={missing}")

    title_gaps = []
    source_gaps = []
    unresolved_paths = []
    for iid, r in by_id.items():
        title = r["title"]
        if title not in emap:
            # allow if map has abbreviated form in register cell
            m = re.search(rf"\| {re.escape(iid)} \| ([^|]+) \| ([^|]+) \|", emap)
            map_title = m.group(2).strip() if m else ""
            if map_title != title:
                title_gaps.append((iid, title, map_title))
        for tok in [t.strip() for t in r["evidence_sources"].split(";") if t.strip()]:
            rel, ok = resolve_source(tok)
            if not ok:
                unresolved_paths.append((iid, tok))
            # map should mention basename at least
            base = Path(tok).name
            if base not in emap and tok not in emap:
                source_gaps.append((iid, tok))

    print(f"title gaps vs CSV: {len(title_gaps)}")
    for g in title_gaps:
        print(" ", g)
    print(f"source tokens missing from map prose: {len(source_gaps)}")
    for g in source_gaps[:25]:
        print(" ", g)
    print(f"unresolved package paths: {len(unresolved_paths)}")
    for g in unresolved_paths:
        print(" ", g)

    # Deep-dive inject sets
    for label, ids in {
        "A": [f"INJ-0{i}" for i in range(21, 29)],
        "B": [f"INJ-0{i}" for i in range(37, 45)],
        "C": [f"INJ-0{i}" for i in range(51, 59)],
    }.items():
        sec = emap
        absent = [i for i in ids if i not in sec]
        print(f"Workflow {label} injects in file: {len(ids)-len(absent)}/{len(ids)} absent={absent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
