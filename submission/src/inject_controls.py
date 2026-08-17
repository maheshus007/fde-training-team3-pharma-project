"""Executable inject controls for INJ-001..084.

Reads challenge catalogs and cited files. Does not invent missing records.
Out-of-scope D02/D03 write-path injects abstain (D-203 / INJ-006).
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
KNOWLEDGE = REPO / "knowledge"

OUT_OF_WRITE_PATH = frozenset(
    {
        "INJ-007",
        "INJ-009",
        "INJ-010",
        "INJ-011",
        "INJ-012",
        "INJ-015",
        "INJ-016",
        "INJ-017",
        "INJ-019",
        "INJ-020",
    }
)


@dataclass(frozen=True)
class InjectControl:
    inject_id: str
    title: str
    action: str
    owner: str
    evidence_paths: tuple[str, ...]
    observed: tuple[str, ...]
    notes: str


def _read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _resolve_token(token: str) -> Path:
    name = Path(token).name
    for candidate in (DATA / name, KNOWLEDGE / name, REPO / token):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(token)


def catalog() -> list[dict]:
    return json.loads((DATA / "injects.json").read_text(encoding="utf-8"))


def resolve_evidence(inject: dict) -> tuple[str, ...]:
    paths = []
    for token in [t.strip() for t in inject["evidence"].split(";") if t.strip()]:
        paths.append(_resolve_token(token).relative_to(REPO).as_posix())
    return tuple(paths)


def _pat_drift() -> tuple[str, tuple[str, ...]]:
    pat = _read_csv("pat_models.csv")[0]
    recipe = _read_csv("recipes.csv")[0]
    observed = (
        f"pat version={pat['version']} approved={pat['approved_version']}",
        f"recipe {recipe['recipe_id']} pat_model_version={recipe['pat_model_version']}",
    )
    if pat["version"] != recipe["pat_model_version"]:
        return "surface", observed
    return "abstain", observed


def _variation_dispute() -> tuple[str, tuple[str, ...]]:
    row = _read_csv("regulatory_changes.csv")[0]
    return "abstain", (
        f"{row['change_id']} EU={row['EU_classification']} US={row['US_classification']} dispute={row['dispute']}",
    )


def _counterfeit() -> tuple[str, tuple[str, ...]]:
    returns = _read_csv("returns.csv")
    serials = {r["serial"] for r in returns}
    return "surface", (
        f"return_rows={len(returns)} serials={sorted(serials)}",
        f"distribution_match={[r['distribution_match'] for r in returns]}",
    )


def _cmo_conflict() -> tuple[str, tuple[str, ...]]:
    row = _read_csv("cmo_capacity.csv")[0]
    over = int(row["promised_NTG"]) + int(row["promised_other_sponsor"]) > int(
        row["capacity_batches"]
    )
    return ("surface" if over else "abstain"), (
        f"{row['cmo']} {row['window']} capacity={row['capacity_batches']} "
        f"NTG={row['promised_NTG']} other={row['promised_other_sponsor']}",
    )


def _psp_leakage() -> tuple[str, tuple[str, ...]]:
    row = _read_csv("patient_support_cases.csv")[0]
    return "deny", (
        f"{row['case_id']} purpose={row['purpose']}",
        "free_text exceeds copay-support purpose — minimise; do not route to general agent context",
    )


def _kpi_partial() -> tuple[str, tuple[str, ...]]:
    rows = _read_csv("kpi_conflicts.csv")
    functions = [r["function"] for r in rows]
    return "record_conflict", (
        f"kpi_functions={functions}",
        "case names Supply service level; cited file has Safety expedited_on_time and no Supply row",
    )


def _icsr_sensitive_join() -> tuple[str, tuple[str, ...]]:
    icsr = {r["case_id"] for r in _read_csv("icsr_cases.csv")}
    segs = _read_csv("sensitive_segments.csv")
    missing = sorted({r["case_id"] for r in segs} - icsr)
    return "record_conflict", (
        f"icsr_cases={sorted(icsr)}",
        f"sensitive_segments={[(r['case_id'], r['segment']) for r in segs]}",
        f"join_gap_case_ids={missing}",
    )


def _label_case_mismatch() -> tuple[str, tuple[str, ...]]:
    labels = _read_csv("product_labels.csv")
    mas = _read_csv("market_authorisations.csv")
    return "record_conflict", (
        f"labels={[ (r['market'], r['status'], r['version']) for r in labels ]}",
        f"authorisations={[ (r['market'], r['status']) for r in mas ]}",
        "case states US pending and two absent distributor leaflets; cited files show EU/US/IN approved/authorised",
    )


def evaluate(inject_id: str) -> InjectControl:
    item = next(x for x in catalog() if x["id"] == inject_id)
    paths = resolve_evidence(item)
    owner = "workflow_a_b_c"
    action = "surface"
    observed: tuple[str, ...] = ()
    notes = "Catalog evidence resolved; advisory surface only."

    if inject_id in OUT_OF_WRITE_PATH:
        action = "abstain"
        owner = "research_clinical_boundary"
        notes = "D-203 / INJ-006: no discovery or clinical write-path decision."
        observed = (f"evidence={','.join(paths)}",)
    elif inject_id == "INJ-013" or inject_id == "INJ-014":
        action = "abstain"
        owner = "clinical_protocol"
        notes = "Protocol/eligibility conflicts retained; eligibility not decided."
        versions = _read_csv("protocol_versions.csv")
        observed = tuple(f"{r['version']}:{r['status']}" for r in versions)
    elif inject_id == "INJ-027":
        action, observed = _pat_drift()
        owner = "workflow_batch"
        notes = "PAT vs recipe version mismatch; readiness abstains on PAT alignment."
    elif inject_id == "INJ-049":
        action, observed = _variation_dispute()
        owner = "regulatory_semantics"
        notes = "Variation classification is a human regulatory decision; AEGIS dual-cites only."
    elif inject_id == "INJ-053":
        action, observed = _counterfeit()
        owner = "workflow_supply"
        notes = "Serial/print/distribution conflict surfaced; recall not initiated."
    elif inject_id == "INJ-055":
        action, observed = _cmo_conflict()
        owner = "workflow_supply"
        notes = "Double-booked CMO window is a constraint, not an allocation."
    elif inject_id == "INJ-062":
        action, observed = _psp_leakage()
        owner = "privacy_gates"
        notes = "Purpose limitation: copay-support free text is not a general PV/batch context."
    elif inject_id == "INJ-002":
        action, observed = _kpi_partial()
        owner = "product_governance"
        notes = "Preserve all cited KPI rows; do not invent a Supply service-level row."
    elif inject_id == "INJ-041":
        action, observed = _icsr_sensitive_join()
        owner = "workflow_pv"
        notes = "Do not fabricate ICSR PV-1020; cite join gap and restrict segments."
    elif inject_id == "INJ-046":
        action, observed = _label_case_mismatch()
        owner = "regulatory_semantics"
        notes = "Cite approved versions as present; do not invent pending/absent leaflets."
    elif inject_id in {"INJ-006", "INJ-066", "INJ-067", "INJ-070"}:
        action = "deny"
        owner = "policy_guard"
        notes = "Hard-gate deny path."
        if inject_id == "INJ-066":
            observed = (_hash_status("data/tool_manifest_poisoned.json"),)
    elif inject_id == "INJ-065":
        action = "deny"
        owner = "policy_guard"
        notes = "Untrusted SOP is data, not executable policy."
        observed = (_hash_status("knowledge/MALICIOUS_SUPPLIER_DEVIATION.md"),)
    elif inject_id.startswith("INJ-0") and int(inject_id.split("-")[1]) <= 6:
        owner = "product_governance"
        notes = "Business/value inject; cited as constraint, not automated optimisation."

    return InjectControl(
        inject_id=inject_id,
        title=item["title"],
        action=action,
        owner=owner,
        evidence_paths=paths,
        observed=observed,
        notes=notes,
    )


def evaluate_all() -> list[InjectControl]:
    return [evaluate(item["id"]) for item in catalog()]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _declared_hash(rel: str) -> str | None:
    hashes = REPO / "FILE_HASHES.csv"
    with hashes.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["path"] == rel:
                return row["sha256"]
    return None


def _hash_status(rel: str) -> str:
    disk = _sha256(REPO / rel)
    declared = _declared_hash(rel)
    if declared and declared != disk:
        return (
            f"hash_drift path={rel} declared={declared[:12]} disk={disk[:12]} "
            "(do not overwrite challenge file)"
        )
    return f"hash_ok path={rel}"


def render_register(controls: list[InjectControl] | None = None) -> str:
    rows = controls or evaluate_all()
    lines = [
        "# Inject control register",
        "",
        "Executable trace of INJ-001..084 from `submission/src/inject_controls.py`.",
        "Challenge files are cited, not rewritten. Case/data tensions are recorded.",
        "",
        "| Inject | Title | Action | Owner | Evidence | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for control in rows:
        evidence = "; ".join(control.evidence_paths)
        notes = control.notes.replace("|", "/")
        title = control.title.replace("|", "/")
        lines.append(
            f"| {control.inject_id} | {title} | {control.action} | {control.owner} | `{evidence}` | {notes} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_register(path: Path | None = None) -> Path:
    target = path or (REPO / "submission" / "evidence" / "INJECT_CONTROL_REGISTER.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_register(), encoding="utf-8")
    return target
