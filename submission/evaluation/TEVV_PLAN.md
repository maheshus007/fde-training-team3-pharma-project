# Participant TEVV Plan — AEGIS-PHARMA

| Field | Entry |
|---|---|
| Owner | Team 3 — Evaluation |
| Version / date | 1.1 / 2026-08-12 |
| Related | `evaluation/EVALUATION_PLAN.md`; artefact `22_EVALUATION_SCORECARD.md` |
| Runtime default | AI-disabled deterministic (D-004) |

## Suite map

| # | Dataset | Graders / controls | Gate |
|---|---|---|---|
| 1 | `S01_business_baseline.json` | thresholds | Soft |
| 2 | `S02_evidence_fidelity_provenance.json` | evidence, temporal_unit, authority | Hard |
| 3 | `S03_gxp_and_safety_boundaries.json` | prohibited_action, trajectory | Hard |
| 4 | `S04_data_integrity_audit_trail.json` | schema, evidence | Hard |
| 5 | `S05_retrieval_authority_supersession.json` | security, authority | Hard |
| 6 | `S06_structured_output_abstention.json` | schema; HUMAN_REVIEW_RUBRIC | Hard |
| 7 | `S07_pv_duplicate_clock_terminology.json` | schema, temporal_unit, subgroup | Hard |
| 8 | `S08_agent_path_tool_authorization.json` | trajectory, security | Hard |
| 9 | `S09_privacy_leakage_cross_border.json` | security | Hard |
| 10 | `S10_subgroup_language_usability.json` | subgroup | Subgroup |
| 11 | `S11_latency_token_cost_dow.json` | latency_cost | Budget |
| 12 | `S12_model_substitution_outage_rollback.json` | JUDGE_CONTROLS; AI-disabled | Continuity |

## Named deliverables

Golden / edge / adversarial / failure+outage+recovery / subgroup / thresholds / regression / human rubric / release-gate policy. Deterministic graders primary; no LLM judge (`JUDGE_CONTROLS.md`).

## Commands

`python submission/scripts/{setup,test,evaluate,reset}.py`
