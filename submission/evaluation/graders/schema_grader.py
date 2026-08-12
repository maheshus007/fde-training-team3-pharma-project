"""Schema grader — versioned workflow contracts with additionalProperties denial."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SRC = Path(__file__).resolve().parents[2] / "src"
FIXTURES = Path(__file__).resolve().parents[2] / "tests" / "fixtures"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from contracts import (  # noqa: E402
    WORKFLOW_SCHEMAS,
    resolve_contracts_dir,
    validate,
    validate_named,
    validate_workflow_response,
)


def validate_against_schema_file(payload: dict[str, Any], schema_name: str) -> list[str]:
    """Scorecard-compatible alias: validate payload dict against a schema file."""
    base = resolve_contracts_dir()
    schema_path = base / schema_name
    if not schema_path.is_file():
        alt = FIXTURES / schema_name
        schema_path = alt if alt.is_file() else schema_path
    if not schema_path.is_file():
        return [f"$: schema file not found: {schema_name}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validate(payload, schema, contracts_dir=schema_path.parent)


def grade_schema(payload: dict[str, Any], schema_name: str | None = None) -> dict[str, Any]:
    """Pass when payload validates against the workflow schema (no unknown props)."""
    workflow = payload.get("workflow")
    if schema_name is None:
        if workflow not in WORKFLOW_SCHEMAS:
            return {
                "grader": "schema",
                "result": "fail",
                "gate": "schema_unresolved",
                "detail": f"cannot resolve schema for workflow {workflow!r}",
            }
        schema_name = WORKFLOW_SCHEMAS[workflow]
    if isinstance(workflow, str) and workflow in WORKFLOW_SCHEMAS:
        errors = validate_workflow_response(payload)
    else:
        errors = validate_against_schema_file(payload, schema_name)
    if errors:
        return {
            "grader": "schema",
            "result": "fail",
            "gate": "schema_violation",
            "detail": "; ".join(errors[:12]),
            "schema": schema_name,
        }
    return {
        "grader": "schema",
        "result": "pass",
        "gate": "schema_conformant",
        "detail": f"valid against {schema_name}",
        "schema": schema_name,
    }


def grade_schema_sample(sample_name: str, schema_name: str) -> dict[str, Any]:
    """Grade a named contract sample file."""
    errors = validate_named(sample_name, schema_name)
    if errors:
        return {
            "grader": "schema",
            "result": "fail",
            "gate": "schema_violation",
            "detail": "; ".join(errors[:12]),
            "schema": schema_name,
            "sample": sample_name,
        }
    return {
        "grader": "schema",
        "result": "pass",
        "gate": "schema_conformant",
        "detail": f"{sample_name} valid against {schema_name}",
        "schema": schema_name,
        "sample": sample_name,
    }
