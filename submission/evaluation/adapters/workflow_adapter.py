"""Adapt package public fixtures to workflow contract names and schemas.

Does not invent regulated decisions. Read-only fixture loading + schema mapping.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PACKAGE_EVAL = ROOT / "evaluation"
SUBMISSION_EVAL = ROOT / "submission" / "evaluation"

# Package workflows → contract id
WORKFLOW_TO_CONTRACT = {
    "batch": "batch_evidence",
    "pv": "pv_intake",
    "supply": "supply_options",
    "security": "gate_non_executing",
    "reliability": "gate_non_executing",
    "privacy": "gate_non_executing",
    "integration": "gate_non_executing",
    "agent": "gate_non_executing",
    "finops": "gate_non_executing",
    "clinical": "gate_non_executing",
}

PACKAGE_SCHEMA_BY_CONTRACT = {
    "batch_evidence": "batch_response.schema.json",
    "pv_intake": "pv_response.schema.json",
    "supply_options": "supply_response.schema.json",
}

PARTICIPANT_SCHEMA_BY_CONTRACT = {
    "gate_non_executing": "gate_response.schema.json",
}

# Deep path implemented for core + security/privacy/agent gate indexing.
# reliability/finops/integration/clinical remain labelled not_implemented.
IMPLEMENTED_WORKFLOWS = frozenset({"batch", "pv", "supply", "security", "privacy", "agent"})


@dataclass(frozen=True)
class AdaptedFixture:
    scenario_id: str
    package_workflow: str
    contract_workflow: str
    schema_name: str
    contract_version: str
    input_hash: str
    fixture_path: str
    authorized_context: dict[str, Any]
    evidence_references: list[str]
    focus: list[str]
    implemented: bool
    notes: str


class WorkflowAdapter:
    """Load PUB-* fixtures and resolve which contract applies."""

    def __init__(self, package_eval: Path | None = None) -> None:
        self.package_eval = package_eval or PACKAGE_EVAL
        self.fixtures_dir = self.package_eval / "public_fixtures"
        self.scenarios_path = self.package_eval / "public_scenarios.json"
        self.participant_contracts = SUBMISSION_EVAL / "contracts"

    def list_scenario_ids(self) -> list[str]:
        scenarios = json.loads(self.scenarios_path.read_text(encoding="utf-8"))
        return [str(s["id"]) for s in scenarios]

    def load_fixture(self, scenario_id: str) -> dict[str, Any]:
        path = self.fixtures_dir / f"{scenario_id}.json"
        if not path.is_file():
            raise FileNotFoundError(path)
        return json.loads(path.read_text(encoding="utf-8"))

    def _schema_for(self, contract: str) -> tuple[str, str]:
        if contract in PACKAGE_SCHEMA_BY_CONTRACT:
            name = PACKAGE_SCHEMA_BY_CONTRACT[contract]
            return name, "package:1.0"
        name = PARTICIPANT_SCHEMA_BY_CONTRACT[contract]
        schema_path = self.participant_contracts / name
        version = "participant:1.0"
        if schema_path.is_file():
            doc = json.loads(schema_path.read_text(encoding="utf-8"))
            props = doc.get("properties") or {}
            sv = props.get("schema_version") or {}
            if isinstance(sv, dict) and sv.get("const"):
                version = f"participant:{sv['const']}"
        return name, version

    def adapt(self, scenario_id: str) -> AdaptedFixture:
        raw = self.load_fixture(scenario_id)
        scenario = raw.get("scenario") or {}
        package_workflow = str(scenario.get("workflow") or raw.get("workflow") or "batch")
        contract = WORKFLOW_TO_CONTRACT.get(package_workflow, "gate_non_executing")
        schema_name, contract_version = self._schema_for(contract)
        blob = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode("utf-8")
        input_hash = hashlib.sha256(blob).hexdigest()
        implemented = package_workflow in IMPLEMENTED_WORKFLOWS
        notes = ""
        if not implemented:
            notes = f"Fixture {scenario_id} workflow={package_workflow} recorded as not_implemented for deep path"
        if contract == "gate_non_executing":
            notes = (notes + " " if notes else "") + "Uses participant gate_response.schema.json (non-executing)"
        return AdaptedFixture(
            scenario_id=scenario_id,
            package_workflow=package_workflow,
            contract_workflow=contract,
            schema_name=schema_name,
            contract_version=contract_version,
            input_hash=input_hash,
            fixture_path=str((self.fixtures_dir / f"{scenario_id}.json").relative_to(ROOT)).replace(
                "\\", "/"
            ),
            authorized_context=dict(raw.get("authorized_context") or {}),
            evidence_references=list(raw.get("evidence_references") or []),
            focus=list(scenario.get("focus") or []),
            implemented=implemented,
            notes=notes.strip(),
        )


def adapt_public_fixture(scenario_id: str) -> AdaptedFixture:
    return WorkflowAdapter().adapt(scenario_id)
