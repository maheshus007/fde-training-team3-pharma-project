#!/usr/bin/env python3
"""Run deterministic evaluation; write evidence + regression/scorecard.

Does not modify package evaluation/ challenge evidence.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "submission"
SRC = SUBMISSION / "src"
EVAL_HARNESS = SUBMISSION / "evaluation"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(EVAL_HARNESS))

from adapters.workflow_adapter import WorkflowAdapter  # noqa: E402
from contracts import load_json  # noqa: E402
from graders.authority_grader import grade_authority  # noqa: E402
from graders.evidence_grader import grade_evidence  # noqa: E402
from graders.latency_cost_grader import grade_latency_cost  # noqa: E402
from graders.prohibited_action_grader import grade_prohibited_actions  # noqa: E402
from graders.schema_grader import grade_schema  # noqa: E402
from graders.security_grader import grade_security  # noqa: E402
from graders.subgroup_grader import grade_subgroup  # noqa: E402
from graders.temporal_unit_grader import grade_temporal_unit  # noqa: E402
from graders.trajectory_grader import grade_trajectory  # noqa: E402

IMPLEMENTATION_VERSION = "submission-evaluation/1.0"
PACKAGE_CONTRACT_VERSION = "package:1.0"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _base_row(**kwargs: object) -> dict:
    row = {
        "implementation_version": IMPLEMENTATION_VERSION,
        "contract_version": PACKAGE_CONTRACT_VERSION,
        "timestamp": _now(),
        "runtime_mode": "ai_disabled_deterministic",
    }
    row.update(kwargs)
    return row


def grade_payload(payload: dict, workflow: str) -> list[dict]:
    return [
        grade_schema(payload),
        grade_authority(payload),
        grade_evidence(payload),
        grade_temporal_unit(payload),
        grade_trajectory(payload),
        grade_prohibited_actions(payload, workflow),
        grade_security(payload),
        grade_subgroup(payload),
        grade_latency_cost(payload),
    ]


def evaluate_contract_samples() -> list[dict]:
    golden = json.loads((EVAL_HARNESS / "datasets" / "golden_set.json").read_text(encoding="utf-8"))
    rows: list[dict] = []
    for item in golden["positive"]:
        payload = load_json(item["sample"])
        grades = grade_payload(payload, item["workflow"])
        overall = "pass" if all(g["result"] == "pass" for g in grades) else "fail"
        rows.append(
            _base_row(
                dataset="GOLDEN-CONTRACT",
                cohort=item["sample"],
                scenario_id=item["sample"],
                workflow=item["workflow"],
                grader="full_suite",
                threshold="all graders pass",
                observed_result=overall,
                gate_result="schema_conformant" if overall == "pass" else "blocked",
                grader_detail=grades,
                evidence_path=f"evaluation/contract_samples/{item['sample']}",
                reviewer_role={
                    "batch_evidence": "EU QP",
                    "pv_intake": "Safety Physician",
                    "supply_options": "Supply Governance Board",
                }.get(item["workflow"], "authorized reviewer"),
            )
        )
    for item in golden["negative"]:
        payload = load_json(item["sample"])
        grades = grade_payload(payload, item["workflow"])
        prohibited = next(g for g in grades if g["grader"] == "prohibited_action")
        schema = next(g for g in grades if g["grader"] == "schema")
        overall = "pass" if prohibited["result"] == "fail" or schema["result"] == "fail" else "fail"
        rows.append(
            _base_row(
                dataset="EDGE-PROHIBITED",
                cohort=item["sample"],
                scenario_id=item["sample"],
                workflow=item["workflow"],
                grader="prohibited_action+schema",
                threshold="prohibited fields / schema must fail closed",
                observed_result=overall,
                gate_result="fail_closed" if overall == "pass" else "leak",
                grader_detail=[prohibited, schema],
                evidence_path=f"evaluation/contract_samples/{item['sample']}",
                reviewer_role={
                    "batch_evidence": "EU QP",
                    "pv_intake": "Safety Physician",
                    "supply_options": "Supply Governance Board",
                }.get(item["workflow"], "authorized reviewer"),
            )
        )
    return rows


def index_public_fixtures() -> list[dict]:
    adapter = WorkflowAdapter()
    rows: list[dict] = []
    for scenario_id in adapter.list_scenario_ids():
        adapted = adapter.adapt(scenario_id)
        rows.append(
            _base_row(
                dataset="GOLDEN-PUB",
                cohort=scenario_id,
                scenario_id=scenario_id,
                workflow=adapted.package_workflow,
                grader="fixture_index",
                threshold="fixture loadable; input hash recorded",
                observed_result="pass" if adapted.implemented else "not_implemented",
                gate_result="indexed" if adapted.implemented else "partial_coverage",
                input_hash=adapted.input_hash,
                contract_workflow=adapted.contract_workflow,
                contract_version=adapted.contract_version,
                schema=adapted.schema_name,
                focus=adapted.focus,
                notes=adapted.notes,
                evidence_path=adapted.fixture_path,
                reviewer_role={
                    "batch": "EU QP",
                    "pv": "Safety Physician",
                    "supply": "Supply Governance Board",
                    "security": "CISO",
                    "privacy": "DPO",
                }.get(adapted.package_workflow, "authorized reviewer"),
            )
        )
    return rows


def _suite_dataset_paths() -> list[Path]:
    # Explicit S01–S12 pattern (Windows case-insensitive glob would match scorecard.json).
    return sorted((EVAL_HARNESS / "datasets").glob("S[0-9][0-9]_*.json"))


def index_suite_datasets() -> list[dict]:
    rows: list[dict] = []
    for path in _suite_dataset_paths():
        doc = json.loads(path.read_text(encoding="utf-8"))
        suite_id = doc.get("suite_id", path.stem.split("_", 1)[0])
        for case in doc.get("cases") or []:
            input_path = case.get("input_path") or ""
            exists = (ROOT / input_path).is_file() if input_path else False
            rows.append(
                _base_row(
                    dataset=suite_id,
                    cohort=case.get("case_id"),
                    scenario_id=case.get("case_id"),
                    workflow=doc.get("name"),
                    grader=",".join(doc.get("graders") or []),
                    threshold=case.get("expect"),
                    observed_result="pass" if exists else "fail",
                    gate_result=("documented" if input_path.endswith(".md") else "suite_indexed")
                    if exists
                    else "missing_input",
                    suite_gate=doc.get("gate"),
                    kind=case.get("kind"),
                    inject=case.get("inject"),
                    focus=case.get("focus"),
                    reviewer_role=case.get("reviewer_role"),
                    evidence_path=input_path,
                )
            )
    return rows


def index_named_sets() -> list[dict]:
    """Index EVALUATION_PLAN / DoD named sets (edge, adversarial, failure/outage/recovery)."""
    rows: list[dict] = []
    specs = [
        ("EDGE-CASE", "edge_case_set.json", "items"),
        ("ADVERSARIAL", "adversarial_set.json", "items"),
    ]
    for dataset, filename, key in specs:
        doc = json.loads((EVAL_HARNESS / "datasets" / filename).read_text(encoding="utf-8"))
        for item in doc.get(key) or []:
            rel = item.get("path") or ""
            exists = (ROOT / rel).is_file() if rel else False
            rows.append(
                _base_row(
                    dataset=dataset,
                    cohort=item.get("id"),
                    scenario_id=item.get("id"),
                    workflow=item.get("focus"),
                    grader="set_index",
                    threshold=item.get("expect"),
                    observed_result="pass" if exists else "fail",
                    gate_result="indexed" if exists else "missing_input",
                    evidence_path=rel,
                    reviewer_role="authorized reviewer",
                )
            )

    fr = json.loads((EVAL_HARNESS / "datasets" / "failure_recovery_set.json").read_text(encoding="utf-8"))
    for section in ("failure", "outage", "recovery"):
        for item in fr.get(section) or []:
            rel = item.get("path") or ""
            exists = (ROOT / rel).is_file() if rel else False
            rows.append(
                _base_row(
                    dataset=section.upper(),
                    cohort=item.get("id"),
                    scenario_id=item.get("id"),
                    workflow=section,
                    grader=item.get("grader") or "set_index",
                    threshold=item.get("expect"),
                    observed_result="pass" if exists else "fail",
                    gate_result="indexed" if exists else "missing_input",
                    evidence_path=rel,
                    reviewer_role="authorized reviewer",
                )
            )
    return rows


def _append_regression(summary: dict) -> None:
    path = EVAL_HARNESS / "datasets" / "regression_history.json"
    hist = {"version": "1.0", "description": "Append-only evaluate history; fail blocks release.", "entries": []}
    if path.exists():
        hist = json.loads(path.read_text(encoding="utf-8"))
    hist.setdefault("entries", []).append(
        {
            "timestamp": summary["generated_at"],
            "counts": summary["counts"],
            "hard_gate_blocked": summary["counts"]["fail"] > 0,
            "implementation_version": IMPLEMENTATION_VERSION,
            "evidence_path": "submission/evidence/evaluation_results.json",
            "policy": "RELEASE_GATE_POLICY.md",
        }
    )
    # Keep last 20 entries only (history, not noise dump)
    hist["entries"] = hist["entries"][-20:]
    path.write_text(json.dumps(hist, indent=2) + "\n", encoding="utf-8")


def _refresh_scorecard(summary: dict) -> None:
    path = EVAL_HARNESS / "datasets" / "scorecard.json"
    card = {
        "version": "1.0",
        "related_artefact": "submission/artefacts/22_EVALUATION_SCORECARD.md",
        "generated_by": "submission/scripts/evaluate.py",
        "implementation_version": IMPLEMENTATION_VERSION,
        "poc_demo_threshold": {
            "zero_fail_on_implemented": True,
            "not_implemented_allowed_if_labelled": True,
        },
        "ai_pilot_threshold": {
            "fixtures_15_of_15": False,
            "model_integrity_green": False,
        },
        "current": {
            "generated_at": summary["generated_at"],
            "counts": summary["counts"],
            "hard_gate_status": "blocked" if summary["counts"]["fail"] > 0 else "clear",
            "poc_demo_ready": summary["counts"]["fail"] == 0,
            "ai_pilot_ready": False,
        },
    }
    path.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    results = (
        evaluate_contract_samples()
        + index_public_fixtures()
        + index_suite_datasets()
        + index_named_sets()
    )
    out_dir = SUBMISSION / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "evaluation_results.json"
    thresholds = json.loads((EVAL_HARNESS / "datasets" / "thresholds.json").read_text(encoding="utf-8"))
    suite_files = [p.name for p in _suite_dataset_paths()]
    summary = {
        "generated_at": _now(),
        "harness": "submission/evaluation",
        "implementation_version": IMPLEMENTATION_VERSION,
        "package_evaluation_immutable": True,
        "tevv_plan": "submission/evaluation/TEVV_PLAN.md",
        "release_gate_policy": "submission/evaluation/RELEASE_GATE_POLICY.md",
        "suite_datasets": suite_files,
        "grader_suite": [
            "schema",
            "authority",
            "evidence",
            "temporal_unit",
            "trajectory",
            "prohibited_action",
            "security",
            "subgroup",
            "latency_cost",
        ],
        "thresholds": thresholds,
        "counts": {
            "total": len(results),
            "pass": sum(1 for r in results if r["observed_result"] == "pass"),
            "fail": sum(1 for r in results if r["observed_result"] == "fail"),
            "not_implemented": sum(1 for r in results if r["observed_result"] == "not_implemented"),
        },
        "results": results,
    }
    out_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _append_regression(summary)
    _refresh_scorecard(summary)
    print(json.dumps(summary["counts"], indent=2))
    print(f"wrote {out_path.relative_to(ROOT)}")
    if summary["counts"]["fail"] > 0:
        print("RELEASE BLOCKED — hard-gate fail (see RELEASE_GATE_POLICY.md)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
