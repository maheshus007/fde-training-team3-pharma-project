# Threat and Abuse Model

> Participant working artefact for Project AEGIS-PHARMA. Analysis cites challenge evidence; enforcement lives under `submission/src/policy_guard.py`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Security / privacy lead |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Architecture/integration lead; GxP/quality lead; Evaluation/reliability lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-065..070, INJ-076; WA-05; D-008, D-009, D-014, D-404 |

## Purpose

Define abuse cases against AEGIS agentic and retrieval surfaces, map each to deny-by-default controls and negative tests, and record residual risk so later defence can show hard gates without claiming zero residual attack surface.

Accountable owner: Security/privacy lead. Completion criteria: injection, tool poisoning, stale auth, exfiltration, ransomware, model supply chain, denial-of-wallet, excessive agency and replay each have control + negative test + residual risk entry.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-1601 | `case/INTEGRATED_CASE.md` INJ-065..070, INJ-076 | Case inject catalogue | Threat narratives and evidence pointers | Narrative; details in CSV/JSON |
| E-1602 | `data/tool_manifest_poisoned.json`; `data/tool_catalog.csv` | Challenge fixture (INJ-066) | `batch_status_plus` requests disposition write + postAction | Synthetic poison sample |
| E-1603 | `data/access_cache.csv`; `data/users_entitlements.csv` | Challenge fixture (INJ-067) | contractor_77 revoked in IAM, cache still active | Synthetic |
| E-1604 | `data/ai_use_boundaries.csv` | Executive boundary (INJ-006) | Allowed reconcile/cite vs prohibited release/PV final/allocate | Binding |
| E-1605 | `data/knowledge_catalog.csv`; supplier deviation material | INJ-065 | Untrusted SOP/PDF with hidden ignore-hold instructions | Treat as data |
| E-1606 | `data/model_registry.csv`; `data/model_artifacts.csv` | INJ-070 | Registry hash ≠ deployed hash | Diagnostic finding |
| E-1607 | `data/security_events.csv`; `data/model_usage.csv` | INJ-068, INJ-076 | Exfil attempts; oversized spend pattern | Synthetic events |
| E-1608 | `data/downtime_events.csv`; `data/network_zones.csv` | INJ-069 | OT isolation / degraded MES-QMS | Scenario evidence |
| E-1609 | `submission/src/policy_guard.py`; Phase 4 tests | Team 3 control | Deny prohibited actions, stale auth, poisoned tools, hash mismatch | Participant code |

## 1. Assets and trust boundaries

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| What assets are in scope? | Batch evidence packets; PV narratives; supply option drafts; tool manifests; model packages; entitlement decisions; audit events | Security | This model §1 |
| Trust boundary A — human UI ↔ orchestrator | User purpose, role and object binding checked at execution | Architecture + Security | WA-05; E-1609 |
| Trust boundary B — retrieval ↔ reasoning | Retrieved docs are untrusted data until authority/signature/applicability verified (D-008) | Security | INJ-065; E-1605 |
| Trust boundary C — tool gateway | Only signed, hash-approved, least-privilege tools execute | Security | INJ-066; E-1602 |
| Trust boundary D — IAM ↔ AI gateway | Cache is not authority; IAM state wins at execution | Security | INJ-067; E-1603 |

## 2. Threat actors and abuse cases

| Actor | Abuse case | Primary inject | Impact if uncontrolled |
|---|---|---|---|
| Compromised supplier document author | Hidden instructions in deviation PDF | INJ-065 | Ignore quality holds; false readiness |
| Compromised tool publisher / insider | Poisoned write-capable tool | INJ-066 | Silent disposition change |
| Former contractor / stale session | Use cached entitlement after revoke | INJ-067 | Unauthorized access or action attempt |
| Curious or malicious affiliate user | Cross-affiliate identifiable narrative pull | INJ-068 | Privacy breach |
| Ransomware operator / OT incident | Force degraded evidence paths | INJ-069 | Incomplete batch evidence under pressure |
| Model supply-chain attacker | Swap model artifact hash | INJ-070 | Unapproved inference behaviour |
| Cost abuser / buggy client | Oversized repeated embedding/inference | INJ-076 | Denial-of-wallet |
| Over-privileged agent design | Excessive agency / replay of side effects | INJ-006 | Prohibited regulated action |

## 3. Prompt/retrieval poisoning

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Threat (INJ-065) | Supplier deviation content instructs model to ignore quality holds | Fact from case | E-1601, E-1605 |
| Control | Isolate retrieval as non-executable data; never promote document text to policy; surface untrusted flag; abstain on actionability | Security (D-008) | WA-05 |
| Negative test | Malicious document must not create executable disposition writes; policy_guard still blocks disposition fields | Evaluation | E-1609; `test_prohibited_actions.py` |
| Residual | Human may still be socially engineered by persuasive summary text | GxP | Forced evidence view (artefact 18) |

## 4. Tool and identity abuse

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Tool poisoning (INJ-066) | Poisoned manifests request disposition write and/or mutating postAction | Fact | E-1602; `submission/tests/fixtures/tool_manifest_poisoned.json` |
| Control | `check_tool_manifest`: require approved hash + signature; deny write/disposition permissions, side_effects, postAction, hidden_default | Security | `test_tool_trust.py` |
| Stale auth (INJ-067) | contractor_77 `iam_state=revoked` with active gateway cache | Fact | E-1603; fixtures under `submission/tests/fixtures/` |
| Control | `check_authorization` / `check_authorization_records` deny revoked or stale cache | Security (D-009) | `test_authorization_freshness.py` |
| Excessive agency | Agent emits disposition/final PV/allocate/ship fields | Boundary E-1604 | `check_workflow_payload`; `test_prohibited_actions.py` |
| Replay | No write tools for regulated side effects; idempotent reads only | Architecture | Contracts + policy_guard |

## 5. Data exfiltration and privacy attacks

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Threat (INJ-068) | Crafted query seeks identifiable narratives across affiliates | Case | E-1607 |
| Control | Purpose binding; affiliate/residency scope; sensitive-segment role gates (INJ-041) | Security + Privacy | Artefact 17 |
| Residual | Privileged insider remains residual; mitigated by audit and SoD | Security | Open residual |

## 6. Supply chain and denial-of-wallet

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Model supply chain (INJ-070) | Deployed hash mismatches registry | Diagnostic | E-1606 |
| Control | `check_model_artifact` requires registry hash == artifact hash | Architecture + Security | `test_tool_trust.py` |
| Ransomware / OT (INJ-069) | Historians isolated; MES/QMS degraded | Case | E-1608 |
| Control | Degraded-mode runbooks; abstain under incomplete evidence; no autonomous disposition | GxP + Ops | Blueprint failure modes |
| Denial-of-wallet (INJ-076) | Repeated oversized submissions inflate spend | Case | E-1607 |
| Control | Per-request budgets; kill switch; prefer deterministic path | Architecture + FinOps | Phase 6 metrics |

## 7. Controls, tests and residual risk

| Threat | Control module | Negative test | Residual risk |
|---|---|---|---|
| INJ-065 injection | Untrusted-data isolation; no policy from docs | Document-as-instruction red-team (Phase 5+) | Persuasion of human reviewer |
| INJ-066 tool poison | `check_tool_manifest` | `test_tool_trust.py` | Novel permission alias evasion |
| INJ-067 stale auth | `check_authorization_records` | `test_authorization_freshness.py` | Clock skew between IAM and gateway |
| INJ-068 exfil | Purpose/scope binding | Scope-denial tests in POC | Privileged insider |
| INJ-069 ransomware | Degraded manual path | Continuity tests later | Incomplete evidence pressure |
| INJ-070 model hash | `check_model_artifact` | Hash mismatch unit test | Signed-but-malicious approved model |
| INJ-076 DoW | Budgets / kill switch | Oversized rejection later | Tuning errors |
| Excessive agency | `check_workflow_payload` | `test_prohibited_actions.py` | New field alias — deny-default + review |
| Replay of side effect | No write tools + deny set | Prohibited suite | None for prohibited writes if policy stays in path |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-1601 | Risk | Permission synonym bypasses denylist | Poisoned tool accepted | Security | Expand denylist on catalog change | Open |
| R-1602 | Assumption | Challenge poisoned manifest represents the attack pattern for tests | Miss novel postAction forms | Security | New poison fixture appears | Accepted |
| R-1603 | Gap | Full cross-affiliate exfil suite not yet coded | Incomplete privacy gate evidence | Privacy | Phase 5–6 | Open |
| R-1604 | Risk | Humans override abstention under schedule pressure (BR-01) | Regulated error | GxP | Defence rehearsal | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| No autonomous prohibited action | `check_workflow_payload` | `test_prohibited_actions.py` | E-1604, E-1609 | Pass |
| Stale cache deny (INJ-067) | `check_authorization_records` | `test_authorization_freshness.py` | E-1603 | Pass |
| Poisoned tool deny (INJ-066) | `check_tool_manifest` | `test_tool_trust.py` | E-1602 | Pass |
| Hash mismatch blocks model (INJ-070) | `check_model_artifact` | `test_tool_trust.py` | E-1606 | Pass |
| Untrusted docs not policy (INJ-065) | D-008 + WA-05 | Design + later red-team | E-1605 | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Architecture/integration lead | Reviewer | Keep policy_guard separate from contracts.py | Confirmed | 2026-08-10 |
| GxP/quality lead | Reviewer | Confirm recall/disposition/quality-status in deny set | Covered in BATCH/SUPPLY sets | 2026-08-10 |
| Evaluation/reliability lead | Reviewer | Require unittest evidence before defence claim | Suite green under `submission/tests` | 2026-08-10 |
