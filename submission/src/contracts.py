"""Workflow contract validation helpers for AEGIS-PHARMA (stdlib only).

Loads evaluation/contracts and evaluation/contract_samples when present;
otherwise uses submission/tests/fixtures/. Enforces additionalProperties denial
and explicit prohibited disposition / causality / side-effect field rejection.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SUBMISSION = Path(__file__).resolve().parents[1]
ROOT = SUBMISSION.parent
EVAL_CONTRACTS = ROOT / "evaluation" / "contracts"
EVAL_SAMPLES = ROOT / "evaluation" / "contract_samples"
LOCAL_FIXTURES = SUBMISSION / "tests" / "fixtures"

WORKFLOW_SCHEMAS = {
    "batch_evidence": "batch_response.schema.json",
    "pv_intake": "pv_response.schema.json",
    "supply_options": "supply_response.schema.json",
}

PROHIBITED_BY_WORKFLOW: dict[str, frozenset[str]] = {
    "batch_evidence": frozenset(
        {
            "batch_disposition",
            "disposition",
            "release_decision",
            "reject_decision",
            "reprocess_decision",
            "recall_decision",
        }
    ),
    "pv_intake": frozenset(
        {
            "final_reportability",
            "causality_assessment",
            "final_causality",
            "final_seriousness",
            "final_expectedness",
            "signal_confirmation",
            "safety_conclusion",
        }
    ),
    "supply_options": frozenset(
        {
            "reservation_id",
            "allocation_id",
            "shipment_id",
            "recall_id",
            "quality_status_change",
            "stock_reservation",
            "stock_allocation",
        }
    ),
}


def resolve_contracts_dir() -> Path:
    if EVAL_CONTRACTS.is_dir() and (EVAL_CONTRACTS / "batch_response.schema.json").is_file():
        return EVAL_CONTRACTS
    if (LOCAL_FIXTURES / "batch_response.schema.json").is_file():
        return LOCAL_FIXTURES
    raise FileNotFoundError("No contract schemas under evaluation/contracts/ or submission/tests/fixtures/")


def resolve_samples_dir() -> Path:
    if EVAL_SAMPLES.is_dir() and (EVAL_SAMPLES / "positive_batch.json").is_file():
        return EVAL_SAMPLES
    if (LOCAL_FIXTURES / "positive_batch.json").is_file():
        return LOCAL_FIXTURES
    raise FileNotFoundError(
        "No contract samples under evaluation/contract_samples/ or submission/tests/fixtures/"
    )


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json(name: str) -> Any:
    """Load a JSON document by filename from samples or contracts dirs (fixtures fallback)."""
    for base in (resolve_samples_dir(), resolve_contracts_dir(), LOCAL_FIXTURES):
        candidate = base / name
        if candidate.is_file():
            return _read(candidate)
    raise FileNotFoundError(name)


def validate(value: Any, schema: dict[str, Any], path: str = "$", contracts_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    base = contracts_dir or resolve_contracts_dir()

    if "$ref" in schema:
        target = _read(base / schema["$ref"])
        return validate(value, target, path, contracts_dir=base)

    typ = schema.get("type")
    if isinstance(typ, list):
        ok = any(
            (t == "null" and value is None)
            or (t == "string" and isinstance(value, str))
            or (t == "object" and isinstance(value, dict))
            or (t == "array" and isinstance(value, list))
            or (t == "boolean" and isinstance(value, bool))
            for t in typ
        )
        if not ok:
            return [f"{path}: wrong type"]
    elif typ == "object" and not isinstance(value, dict):
        return [f"{path}: expected object"]
    elif typ == "array" and not isinstance(value, list):
        return [f"{path}: expected array"]
    elif typ == "string" and not isinstance(value, str):
        return [f"{path}: expected string"]
    elif typ == "boolean" and not isinstance(value, bool):
        return [f"{path}: expected boolean"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: not in enum")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: pattern mismatch")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        item_schema = schema.get("items", {})
        for i, item in enumerate(value):
            errors.extend(validate(item, item_schema, f"{path}[{i}]", contracts_dir=base))

    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errors.append(f"{path}: missing {req}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{path}: additional property {key}")
        for key, item in value.items():
            if key in props:
                errors.extend(validate(item, props[key], f"{path}.{key}", contracts_dir=base))

    return errors


def prohibited_field_errors(payload: dict[str, Any], workflow: str | None = None) -> list[str]:
    wf = workflow or payload.get("workflow")
    if not isinstance(wf, str) or wf not in PROHIBITED_BY_WORKFLOW:
        return [f"$: unknown or missing workflow for prohibited-field check ({wf!r})"]

    errors: list[str] = []
    for key in payload:
        if key in PROHIBITED_BY_WORKFLOW[wf]:
            errors.append(f"$: prohibited field {key}")
    if wf == "supply_options" and payload.get("no_side_effects") is False:
        errors.append("$: no_side_effects must not be false")
    return errors


def validate_workflow_response(payload: dict[str, Any], schema_name: str | None = None) -> list[str]:
    base = resolve_contracts_dir()
    workflow = payload.get("workflow")
    if schema_name is None:
        if workflow not in WORKFLOW_SCHEMAS:
            return [f"$: cannot resolve schema for workflow {workflow!r}"]
        schema_name = WORKFLOW_SCHEMAS[workflow]
    schema = _read(base / schema_name)
    errors = validate(payload, schema, contracts_dir=base)
    if isinstance(payload, dict):
        errors.extend(prohibited_field_errors(payload, workflow if isinstance(workflow, str) else None))
    # Deduplicate
    seen: set[str] = set()
    unique: list[str] = []
    for err in errors:
        if err not in seen:
            seen.add(err)
            unique.append(err)
    return unique


def validate_named(sample_name: str, schema_name: str) -> list[str]:
    """Compat helper used by unittest: load sample + schema, fail closed on prohibited fields."""
    sample = load_json(sample_name)
    base = resolve_contracts_dir()
    # Prefer schema from contracts dir; fall back via load_json
    schema_path = base / schema_name
    schema = _read(schema_path) if schema_path.is_file() else load_json(schema_name)
    errors = validate(sample, schema, contracts_dir=base)
    if isinstance(sample, dict):
        errors.extend(prohibited_field_errors(sample))
    seen: set[str] = set()
    unique: list[str] = []
    for err in errors:
        if err not in seen:
            seen.add(err)
            unique.append(err)
    return unique
