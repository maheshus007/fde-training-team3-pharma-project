# Production Readiness

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v1.1 — 2026-08-12 |
| Reviewers | Pending team review |
| Status | Current |
| Related requirements / ADRs | Artefacts 14, 21, 22, 24, 25; `submission/evaluation/RELEASE_GATE_POLICY.md` |

## Purpose

Records an explicit **NO-GO** for production / supervised AI pilot release, with a checklist of what is green for a deterministic POC defence demo versus what remains red. Accountable owner: CQO. Completion criteria: go/no-go decision is unambiguous and evidence-linked.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2801 | `14_COMPUTER_SOFTWARE_ASSURANCE.md` | Prior | No AI-assisted pilot recommended | CSA |
| E-2802 | `13_GXP_LIFECYCLE_VALIDATION.md` | Prior | VT-1/VT-2 failed | Validation |
| E-2803 | `submission/evidence/test_results.json` | Run 2026-08-12 | 46/46 PASS | POC |
| E-2804 | `submission/evidence/evaluation_results.json` | Run | 63 pass, 0 fail, 4 not_implemented | Suites + PUB; deep NI remain |
| E-2805 | `data/model_artifacts.csv` | Challenge | GXP-SUM-1 integrity fail | Blocker |
| E-2806 | `data/downtime_events.csv` DT-2 | Challenge | AI primary outage open | Ops blocker |
| E-2807 | `data/data_residency.csv` | Challenge | EU→SG violation observed | Privacy blocker |
| E-2808 | `submission/runbooks/*`, `evidence/submission_manifest.csv`, `file_hashes.csv`, `submission/app/` | Participant package | Ops docs, hashes, advisory UI present | Thin UI/a11y proof |

## 1. Readiness checklist

| Area | Deterministic POC demo | AI pilot / production |
|---|---|---|
| Schema contracts | GREEN (E-2803) | Necessary not sufficient |
| Unit/gate/grader tests | GREEN (E-2803) | Required |
| Public fixtures deep coverage | AMBER (4 NI: PUB-10/12/14/15) (E-2804) | RED until closed/waived |
| TEVV harness (S01–S12, graders) | GREEN (artefact 22) | Required |
| Model integrity | N/A (no inference) | RED (E-2805) |
| Validation VT | N/A for non-AI path | RED (E-2802) |
| CSA high-risk functions | Partial (gates coded) | RED (E-2801) |
| UI / a11y / automation-bias | AMBER (app present; a11y study incomplete) | RED |
| Residency | RED in estate (E-2807) | RED |
| AI region availability | Degraded (E-2806) | RED |
| Runbooks under submission/runbooks | GREEN filed (E-2808); drill Partial | RED until drilled |
| Vendor exit rehearsal | RED | RED |
| Manifest/hashes | GREEN (E-2808) | Required |

## 2. Open defects and risk acceptances

| ID | Defect / risk | Accept for POC demo? | Accept for pilot? |
|---|---|---|---|
| D-2801 | VT failures | Yes (demo shows fail-closed) | No |
| D-2802 | Model hash mismatch | Yes (abstain path) | No |
| D-2803 | PUB-10/12/14/15 NI | Yes if labelled | No (unless waived) |
| D-2804 | Residency violation | Disclose only | No |
| D-2805 | UI a11y / bias controls incomplete | Yes for script/Taipy demo | No |
| D-2806 | Formal continuity drill not recorded | Yes with filed runbooks | No |

## 3. Security/privacy/GxP gates

| Gate family | POC status |
|---|---|
| Purpose / token / live IAM / checkpoint | Implemented + tested |
| Tool-manifest trust | Implemented + tested (`policy_guard`, `test_tool_trust`) |
| Privacy DSR/hold | Implemented + tested |
| Model integrity | Implemented (blocks use) |
| Disposition language | Implemented + tested |
| Consent live-check / residency remediation | Not implemented / estate open |

## 4. Performance and capacity

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| POC | Stdlib scripts run end-to-end on fixture scale; S11 latency/cost grader present. | Capstone team | test/evaluate |
| Production capacity | Not characterized; baselines in artefact 23. | Platform | Gap R-2801 |

## 5. Operational support

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Support | TOM (26); runbooks filed (SETUP/OPERATIONS/INCIDENT/AI_DISABLED). | Capstone team | E-2808 |
| Continuity | Deterministic / AI-disabled path executable; drill record open (R-2501). | Platform | artefact 24/25 |

## 6. Release/rollback decision

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Decision | **NO-GO** for production and supervised AI inference pilot. **GO** only for controlled defence demonstration of deterministic fail-closed POC. | CQO | E-2801–E-2808 |
| Rollback | `scripts/reset.py` clears regenerable evaluation evidence only. | Capstone team | reset.py |

## 7. Conditions for go/no-go

**Flip to pilot GO only when all are true:**

1. Model artifacts hash+signature verified for every selectable model  
2. VT-1/VT-2 (or successors) pass; AF items closed or formally risk-accepted by CQO  
3. CSA high-risk functions green  
4. Residency violation remediated or formally accepted with compensating control  
5. PUB fixtures implemented or formally waived  
6. UI a11y + automation-bias controls tested  
7. Incident/AI-disabled runbooks approved and drilled  
8. Vendor exit export mirrors for decision evidence in place  

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2801 | Gap | No production perf/capacity test | Medium | Platform | Before scale | Open |
| R-2802 | Gap | Continuity drill evidence not yet filed (runbooks exist) | Medium | Capstone / Ops | Roadmap 0–30 | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| POC demo readiness | src + scripts + evaluation harness | E-2803/E-2804 | — | GO (demo only) |
| Production readiness | Full checklist §1/§7 | E-2801/E-2802 | — | NO-GO |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | CQO | — | — | — |
