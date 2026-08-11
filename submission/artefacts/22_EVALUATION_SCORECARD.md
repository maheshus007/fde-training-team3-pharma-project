# Evaluation Scorecard

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v0.1 draft — 2026-08-07 |
| Reviewers | Pending team review |
| Status | Draft |
| Related requirements / ADRs | `evaluation/EVALUATION_PLAN.md`; `21_ASSURANCE_CASE.md`; scripts/evaluate.py |

## Purpose

Defines what “good” means for this POC, records current scores against the 15 public fixtures, and sets release thresholds that intentionally **fail** while AI integrity/validation gaps remain. Accountable owner: capstone team / CQO. Completion criteria: every fixture has a recorded outcome; `not_implemented` is not counted as pass.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2201 | `evaluation/PUBLIC_FIXTURE_INDEX.csv` + public_fixtures | Challenge evaluation pack | 15 scenarios across batch/pv/supply/security/reliability/privacy/integration/agent/finops/clinical | Immutable challenge set |
| E-2202 | `submission/evidence/evaluation_results.json` | Generated run | pass=11, fail=0, not_implemented=4 | Honest partial coverage |
| E-2203 | `submission/evidence/test_results.json` | Generated run | 51 unit tests OK; 6 contract samples OK | Unit + schema layer |
| E-2204 | `data/model_performance.csv` | Challenge | Language/subgroup slices for PV-NER-4 / TRN-OMICS-2 | Used as gate inputs, not as our model scores |
| E-2205 | `evaluation/contracts/*.schema.json` | Challenge | Authoritative response contracts | — |

## 1. Evaluation objectives

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Primary objective | Prove fail-closed support behaviour and schema safety — not model accuracy leadership. | Capstone team | E-2201, artefact 21 |
| Secondary | Surface coverage gaps honestly (PUB-10/12/14/15). | Capstone team | E-2202 |

## 2. Datasets and cohorts

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Public fixtures | PUB-01…PUB-15 (E-2201). | Capstone team | E-2201 |
| Unit fixtures | Deterministic cases in `submission/tests/` grounded in SUA-88, PV clusters, SEC-1/2, AR-77, DSR-17. | Capstone team | E-2203 |
| Subgroup cohorts | Language slices from E-2204 — used to justify abstention, not to claim our NER F1. | Capstone team | E-2204 |
| Missing | Participant adversarial document corpus; private hold-out set. | Capstone team | Gap R-2201 |

## 3. Deterministic graders

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Schema grader | `contracts.validate_against_schema_file` | Capstone team | E-2205 |
| Prohibited-language grader | `find_disposition_language` | Capstone team | E-2203 |
| Gate graders | purpose / token / live auth / checkpoint age / privacy hold / model integrity | Capstone team | E-2203 |
| Fixture runner | `scripts/evaluate.py` records scenario_id, input_hash, result, gate_outcome, reviewer_role | Capstone team | E-2202 |

## 4. Human-review rubric

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Roles | EU QP (batch), safety physician (PV), Supply Governance Board (supply), CISO/DPO for gates | Per fixtures | E-2202 |
| Rubric dimensions | Evidence completeness surfaced; contradictions not hidden; no disposition language; abstention reason clear; citations present | Capstone team | Artefacts 04/18 |
| Gap | No scored human-review panel yet — rubric defined, not executed as a study. | Capstone team | Gap R-2202 |

## 5. Safety and prohibited-action gates

| Gate | Current result | Evidence |
|---|---|---|
| Disposition/side-effect language | PASS on workflow tests | E-2203 |
| Cross-affiliate without purpose | PASS | E-2203; PUB-09 |
| Token DoW | PASS | E-2203 |
| Stale IAM | PASS | E-2203; PUB-09 |
| Stale checkpoint | PASS | PUB-13 |
| Unverified model | PASS (abstain) | model gateway tests |
| DSR vs hold | PASS (abstain) | PUB-11 |

## 6. Subgroup and adversarial results

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Language | Out-of-scope languages blocked; English also abstains pending artifact record (R-1004). | Capstone team | E-2204; gateway tests |
| Adversarial | Tool-manifest poison modelled in artefact 16; runtime tool gate not coded; no malicious-doc suite yet. | Capstone team | Gap R-2201 |
| Partial fixtures | PUB-07/08 schema-safe abstention with `partial_coverage` notes (wrong tool for allocation/cold-chain). | Capstone team | E-2202 |

## 7. Release thresholds and regression

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Threshold for **deterministic POC demo** | Unit tests 100% pass; contract samples 100% pass; zero `fail` on implemented fixtures; `not_implemented` allowed if labelled. | Capstone team | E-2202, E-2203 — **met** |
| Threshold for **AI pilot release** | All of above PLUS: 15/15 fixtures implemented or explicitly waived; model integrity green; VT re-pass; a11y + automation-bias UI controls; residency remediated. | CQO | **not met** |
| Regression rule | Any new `fail` or silent conversion of `not_implemented`→`pass` blocks merge. | Capstone team | evaluate.py design |

## Current scorecard (from E-2202)

| Scenario | Workflow | Result | Gate |
|---|---|---|---|
| PUB-01…03 | batch | pass | schema_conformant |
| PUB-04…06 | pv | pass | schema_conformant |
| PUB-07…08 | supply | pass | partial_coverage |
| PUB-09 | security | pass | gate_enforced |
| PUB-10 | reliability | not_implemented | partial_coverage |
| PUB-11 | privacy | pass | abstain_unconfirmed_link |
| PUB-12 | integration | not_implemented | not_implemented |
| PUB-13 | agent | pass | gate_enforced |
| PUB-14 | finops | not_implemented | not_implemented |
| PUB-15 | clinical | not_implemented | not_implemented |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2201 | Gap | No adversarial document evaluation set | Medium | Capstone team | Phase 5 | Open |
| R-2202 | Gap | Human-review rubric not yet scored on a panel | Medium | CQO | Before pilot claim | Open |
| R-2203 | Risk | PUB-07/08 “pass” could be misread as full supply coverage | Medium | Capstone team | Defence | Mitigated by notes |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Honest fixture scoring | evaluate.py | evaluation_results.json | E-2202 | PASS |
| Pilot release threshold | CSA + VT + 15/15 | — | §7 | FAIL (by design) |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | CQO | — | — | — |
