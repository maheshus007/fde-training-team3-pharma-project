# 90-Day Roadmap and Handover

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v1.1 — 2026-08-12 |
| Reviewers | Pending team review |
| Status | Current |
| Related requirements / ADRs | Artefact 28 NO-GO conditions; open R-IDs across 16–28 |

## Purpose

Prioritises the path from “deterministic fail-closed POC” to a state where a supervised pilot *could* be reconsidered, and lists handover inventory for clean-room transfer. Accountable owner: capstone team → named BAU owners. Completion criteria: 0–30 / 31–60 / 61–90 actions are evidence-linked; stop criteria match artefact 28.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2901 | `28_PRODUCTION_READINESS.md` §7 | Prior | Pilot GO conditions | Blocking list |
| E-2902 | `submission/evidence/evaluation_results.json` | Run | 4 fixtures not_implemented (PUB-10/12/14/15) | Code backlog seed |
| E-2903 | Open gaps R-1702, R-1801, R-2201, R-2301, R-2402, R-2501, R-2701, R-2801 | Prior artefacts | Cross-cutting debt | Runbook file gap closed; drill open |
| E-2904 | `data/vendor_contracts.csv` | Contracts | 120-day AI vendor exit | Time box for portability |
| E-2905 | `submission/runbooks/`, `submission/evaluation/`, evidence hashes/manifest | Participant package | Filed ops + TEVV + packaging | — |

## 1. Prioritized backlog

| Priority | Item | Closes |
|---|---|---|
| P0 | Repair model artifact integrity + re-validate AI-EVIDENCE (VT) | E-2901 #1–2 |
| P0 | Live consent check + residency remediation plan execution | Privacy blockers |
| P0 | Record timed AI-disabled / incident drill against filed runbooks | R-2501 / R-2802 |
| P1 | Deep paths: endpoint failover integrity (PUB-10); LIMS adapter (PUB-12) | E-2902 |
| P1 | FinOps cost/task calculator (PUB-14); clinical protocol abstention (PUB-15) | E-2902 |
| P1 | UI a11y + forced evidence acknowledgment (app scaffold exists) | R-1801 |
| P2 | Exit rehearsal within 120 days; expanded adversarial hold-out; competency programme | E-2904; R-2201; R-2701 |

## 2. 0–30 day actions

| Action | Owner | Acceptance |
|---|---|---|
| Freeze inference; operate deterministic mode only | Platform / CQO | Matches current code |
| Drill AI-disabled path once using filed runbooks; file drill note | Capstone / Ops | Evidence under submission/evidence or runbooks |
| Integrity incident on GXP-SUM-1 with vendor | Platform | Hash/signature plan |
| Confirm DSR-17 ↔ LH-44 identity join | DPO | Close R-1702 / R-501 |
| Keep submission_manifest.csv + file_hashes.csv fresh before defence | Capstone | `hash_and_manifest.py` |
| Keep tool allow-list / poison deny enforced (already coded) | CISO / Capstone | `test_tool_trust.py` green |

## 3. 31–60 day actions

| Action | Owner | Acceptance |
|---|---|---|
| Re-run VT; close or risk-accept AF items | Validation | VT green or CQO acceptance doc |
| Implement PUB-10/12/14/15 or waive with CQO signature | Capstone | evaluate.py NI → 0 or waived |
| Residency remediation for ClinicalLake SG replica | DPO / Infra | data_residency re-check |
| Automation-bias UI MVP + keyboard/a11y pass | Product | Usability findings flipped |
| Dual-export eval/observability off AIVENDOR-X | Platform | Exit asset gaps shrink |

## 4. 61–90 day actions

| Action | Owner | Acceptance |
|---|---|---|
| Timed vendor-exit rehearsal (≤120d constraint awareness) | Procurement / Platform | Drill report |
| Competency training for reviewers | CQO | Training records |
| Supervised pilot proposal **only if** artefact 28 §7 all green | CQO | Go/no-go memo |
| Handover clean-room exercise | Capstone → BAU | Recipient runs setup→evaluate unaided |

## 5. Dependencies and owners

| Dependency | Owner |
|---|---|
| Vendor artifact re-sign / re-deploy | AIVENDOR-X + Platform |
| IAM cache TTL policy | CISO |
| Legal hold / DSR process | DPO |
| Validation resources | CQO / Validation |
| Budget for human review (non-zero) | FinOps |

## 6. Handover inventory

| Asset | Location |
|---|---|
| 30 artefacts | `submission/artefacts/` |
| TEVV harness | `submission/evaluation/` (S01–S12, graders, rubrics) |
| Source + tests + scripts | `submission/src|tests|scripts/` |
| App (advisory UI) | `submission/app/` |
| Runbooks | `submission/runbooks/` |
| Machine evidence | `submission/evidence/*` |
| Challenge evidence (read-only) | `data/`, `knowledge/`, `evaluation/` |
| How to run | `submission/README.md`; runbooks/SETUP.md |

## 7. Success and stop criteria

| Type | Criteria |
|---|---|
| Success (90 days) | Runbooks drilled; integrity path clear; fixtures closed/waived; residency plan executing; clean-room handover passed |
| Stop / do not pilot | Any artefact 28 §7 item still red; fabricated eval passes; side-effecting tools enabled; DT-2 “fixed” by unsafe fallback |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2901 | Assumption | BAU owners will be named before day 30 | Medium | Capstone team | A-001 | Open |
| R-2902 | Risk | 90 days insufficient if vendor integrity fix slips | High | Platform | P0 | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Roadmap tied to NO-GO conditions | §1–4 ↔ artefact 28 §7 | Review | E-2901 | PASS (doc) |
| Clean-room handover executable | README + scripts + runbooks | Recipient trial | E-2905 | Pending drill |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | CQO / Programme | — | — | — |
