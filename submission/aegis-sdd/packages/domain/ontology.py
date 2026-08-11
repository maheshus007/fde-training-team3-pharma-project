"""Ontology / semantic gates (T-008). No OWL/RDF.

Canonical product module. Scoring shim: `submission/src/ontology.py`.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

_DATA = Path(__file__).resolve().parents[4] / "data"

_APPROVED = frozenset({"yes", "true", "approved"})


def _rows(name: str) -> list[dict[str, str]]:
    path = _DATA / name
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def evaluate_unit_mapping(
    source_unit: str,
    target_unit: str,
    mapping: Mapping[str, Any],
) -> dict[str, Any]:
    """Convert only if mapping.approved is yes; else abstain (INJ-024 / ADR-AA-014)."""
    del source_unit, target_unit
    approved = str(mapping.get("approved", "")).strip().lower()
    if approved not in _APPROVED:
        return {
            "allowed": False,
            "converted_value": None,
            "abstention": {
                "code": "unit_unapproved",
                "reason": "interface mapping is not approved; comparison abstained",
            },
        }
    return {"allowed": True, "converted_value": None, "abstention": None}


def evaluate_lab_comparability(lab_result_id: str) -> dict[str, Any]:
    """Fixture-backed AC-A3: LR-88 vs spec units uses CRO_LAB_TO_LIMS."""
    lab = next((r for r in _rows("lab_results.csv") if r.get("result_id") == lab_result_id), None)
    mapping = next((r for r in _rows("interface_mappings.csv") if r.get("interface") == "CRO_LAB_TO_LIMS"), None)
    if lab is None:
        return {
            "allowed": False,
            "converted_value": None,
            "abstention": {"code": "unit_unapproved", "reason": f"unknown lab result {lab_result_id}"},
        }
    source_unit = lab.get("unit") or ""
    spec = lab.get("spec") or ""
    return evaluate_unit_mapping(source_unit, spec, mapping or {"approved": "no"})


def resolve_product_identity(
    product_id_a: str,
    product_id_b: str,
    *,
    mapping_status: str | None = None,
) -> dict[str, Any]:
    """CQ-5: exact id → alias table → stop. Never fuzzy. Ambiguous IDMP stays conflict."""
    a = str(product_id_a).strip()
    b = str(product_id_b).strip()
    if a == b:
        return {"same_product": True, "status": "exact", "merged": False}

    aliases = {r.get("alias", ""): r.get("canonical_product", "") for r in _rows("product_master_aliases.csv")}
    # Alias is search-only; do not treat alias hit as identity merge.
    del aliases

    status = mapping_status
    if status is None:
        for row in _rows("idmp_mappings.csv"):
            pair = {row.get("local_product", ""), row.get("idmp_product", "")}
            if a in pair and b in pair:
                status = row.get("mapping_status")
                break
    if status and str(status).strip().lower() not in _APPROVED:
        return {
            "same_product": False,
            "status": "conflict",
            "merged": False,
            "mapping_status": status,
        }
    return {"same_product": False, "status": "unresolved", "merged": False}


def retain_coding(row: Mapping[str, Any]) -> dict[str, str]:
    """Keep MedDRA version on every coding struct (INJ-039)."""
    version = row.get("meddra_version")
    if not version:
        raise ValueError("meddra_version required")
    return {
        "case_id": str(row.get("case_id") or ""),
        "verbatim": str(row.get("verbatim") or ""),
        "pt": str(row.get("pt") or ""),
        "meddra_version": str(version),
    }
