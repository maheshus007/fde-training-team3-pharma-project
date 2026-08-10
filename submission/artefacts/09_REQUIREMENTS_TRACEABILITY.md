# Requirements and Traceability

> Participant working artefact for Project AEGIS-PHARMA. Uniquely identified FR/NFR/GXP/SEC/PRI requirements for Workflows A–C with acceptance criteria and planned tests. Implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product/value lead with Domain/evidence and Evaluation leads |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | GxP/quality; Security/privacy; Architecture/integration |
| Status | Reviewed |
| Related requirements / ADRs | `case/INTEGRATED_CASE.md` §4–5; `data/ai_use_boundaries.csv`; artefacts 04–08; D-001..D-010; D-206; scoring hard gates in `requirements/SCORING_MODEL.md` |

## Purpose

Freeze a traceable requirements baseline for the three mandatory workflows so every material claim maps to acceptance criteria and planned tests before model inference or POC coding expands (D-206).

Accountable owner: Product/value lead. Completion criteria: unique IDs across FR/NFR/GXP/SEC/PRI; each Workflow A–C covered; acceptance criteria and planned test IDs present; change/waiver control defined.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-901 | `case/INTEGRATED_CASE.md` §4–5, §9 | Case | Workflow scope, operating properties, definition of done | Binding narrative |
| E-902 | `data/ai_use_boundaries.csv` | Executive | Allowed vs prohibited actions | Hard gate |
| E-903 | `data/board_requests.csv` BR-01 | Board | −14% lead time; no spec/Quality-authority change | Value constraint |
| E-904 | `data/continuity_requirements.csv` | Continuity | AI-disabled windows; PV manual required | Reliability |
| E-905 | `data/kpi_conflicts.csv` | KPI owners | Conflicting incentives | Guardrail |
| E-906 | `requirements/SCORING_MODEL.md` | Scoring | Hard gates (unit, authz, prohibitions, etc.) | Evaluation |
| E-907 | `submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md` | Phase 1 | Personas and journeys | Design |
| E-908 | `data/decision_rights.csv` | RAPID inputs | Accountable roles vs ai_authority | Governance |
| E-909 | `data/usability_findings.csv` | INJ-073 | Keyboard and colour-only defects | Accessibility |
| E-910 | Artefacts 05–08; `EVIDENCE_MAP.md` | Phase 2 | Domain/evidence model | Design baseline |

## 1. Stakeholder and business requirements

| ID | Statement | Stakeholder | Evidence | Planned test |
|---|---|---|---|---|
| BR-AEGIS-01 | Contribute to BR-01 release lead-time reduction without changing registered specifications or weakening Quality authority | Board / Manufacturing / Quality | E-903 | BEN-01 benefits proxy measure (Phase 6) |
| BR-AEGIS-02 | Deliver measurable value vs no-AI baselines (master_data_repair, rules_workflow) before claiming unique genAI benefit | Process excellence / Product | `no_ai_baselines.csv`; INJ-003 | BEN-02 comparative run |
| BR-AEGIS-03 | Preserve independent local legal accountability (QP, safety officers) under global process pressure | Quality / Safety / INJ-074 | E-908; stakeholder pack | GOV-01 RAPID path review |
| BR-AEGIS-04 | Operate offline with AI-disabled continuity for agreed windows | Reliability / all workflow owners | E-904; INJ-082 | REL-01 outage drill |
| BR-AEGIS-05 | Do not optimize one KPI by suppressing another’s evidence needs | Cross-functional | E-905; INJ-002 | GOV-02 conflict honesty check |

## 2. Functional requirements

### Workflow A — GxP batch evidence reconciliation

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| FR-A-01 | System assembles a Batch Evidence Pack for a selected batch_id with cited source records | Pack lists each fact with source path/record id, authority, effective time | TEST-A-01 pack schema |
| FR-A-02 | System detects genealogy conflicts between MES genealogy and warehouse movements | For NCB204-B24071 / SUA-88, both `missing_branch` and WM-90 issued are shown | TEST-A-02 INJ-021 |
| FR-A-03 | System abstains on lab comparisons when unit mapping is unapproved | LR-88 yields abstain; no silent mg/L→µg/mL convert | TEST-A-03 INJ-024 |
| FR-A-04 | System surfaces OOS/OOT/invalid disagreements without collapsing them | Distinct statuses from lab_results / oos_investigations retained | TEST-A-04 INJ-023 |
| FR-A-05 | System flags QP release-packet gaps (e.g. missing supplier audit commitment) | Gap item references release_packets and supplier_audits | TEST-A-05 INJ-028 |
| FR-A-06 | System outputs readiness assessment only (complete / incomplete / abstain reasons) | No release/reject/reprocess/recall action or API | TEST-A-06 prohibited write |
| FR-A-07 | AI-disabled path performs FR-A-01..05 via rules/fixtures only | Same conflict detections with inference off | TEST-A-07 continuity |

### Workflow B — PV intake and signal support

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| FR-B-01 | System ingests ICSR narratives and emits structured fields with provenance | Output schema includes case_id, verbatim pointers, receipt channels | TEST-B-01 intake schema |
| FR-B-02 | System proposes duplicate clusters with similarity and reason; does not auto-merge | PV-1001–PV-1014 returned as candidate; final merge absent | TEST-B-02 INJ-037 |
| FR-B-03 | System retains MedDRA version on each coding and flags cross-version grouping risk | 27.1 vs 28.0 both visible for related cases | TEST-B-03 INJ-039 |
| FR-B-04 | System reconstructs reporting-clock candidates from conflicting receipts | Vendor/affiliate/global dates shown; no silent single clock | TEST-B-04 INJ-038 |
| FR-B-05 | System presents listedness by source (IB/CCDS/local label) without global collapse | IN local label `listed=no` co-exists with CCDS `yes` | TEST-B-05 INJ-040 |
| FR-B-06 | System segments pregnancy/paediatric sensitive content for elevated roles | Unauthorized role denied segment; authorized sees tagged segment | TEST-B-06 INJ-041 |
| FR-B-07 | System abstains on unauthenticated social-media cases for actionable PV | Authenticity failure surfaced for INJ-042 fixture | TEST-B-07 INJ-042 |
| FR-B-08 | No final seriousness, causality, expectedness, reportability or signal confirmation by system | Tool/catalog excludes those writes/decisions | TEST-B-08 prohibited PV |
| FR-B-09 | Manual/AI-disabled intake path remains available | Continuity requirement for PV satisfied | TEST-B-09 continuity |

### Workflow C — Supply shortage / cold-chain recovery options

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| FR-C-01 | System generates ranked supply options with citations to inventory, quality status, MA and constraints | Each option lists constraint ids from allocation_constraints / related files | TEST-C-01 options schema |
| FR-C-02 | System flags cold-chain logger/pallet/time disputes and abstains on unresolved association | SH-901 / LG-31 P-88 vs P-89 conflict visible | TEST-C-02 INJ-051 |
| FR-C-03 | System includes trial/compassionate/commercial demand channels in option constraints | INJ-056 channels represented; ethics flags visible | TEST-C-03 INJ-056 |
| FR-C-04 | System never creates reservations, allocations or shipments | No reserve/allocate/ship tools; agent_runs draft reservations rejected | TEST-C-04 prohibited supply; INJ-080 |
| FR-C-05 | AI-disabled option enumeration works for continuity window | Rules/spreadsheet path per runbook | TEST-C-05 continuity |

### Cross-workflow functional

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| FR-X-01 | Purpose, user, role and object bound at execution | Missing/stale binding → deny | TEST-X-01 authz bind |
| FR-X-02 | Structured outputs validate against versioned contracts; unknown properties rejected | additionalProperties denial | TEST-X-02 contract |
| FR-X-03 | Idempotency keys prevent duplicate side-effect attempts | Replay safe for read/reconcile | TEST-X-03 idempotency |
| FR-X-04 | Budgets, step limits, checkpoints, rollback and kill switch enforced | Over-budget run stops; kill switch disables inference | TEST-X-04 agent bounds |
| FR-X-05 | Evidence export produces inspection-ready citation pack | Export includes sources for A/B/C run | TEST-X-05 export |

## 3. Non-functional requirements

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| NFR-01 | Offline package mode: no internet/cloud keys required for A–C demos | Full fixture path succeeds disconnected | TEST-NFR-01 offline |
| NFR-02 | Deterministic rules path is default; inference optional and flagged | Config `ai_enabled=false` default in POC | TEST-NFR-02 default path |
| NFR-03 | Latency suitable for interactive review on fixture scale | Pack/cluster/options under agreed local SLA (recorded in Phase 6) | TEST-NFR-03 timing |
| NFR-04 | Cost/token budgets measurable when inference on | Usage logged; denial-of-wallet patterns detectable | TEST-NFR-04 FinOps; INJ-076 |
| NFR-05 | Accessibility: full keyboard operation; warnings not colour-only | INJ-073 defects absent in AEGIS UI | TEST-NFR-05 a11y |
| NFR-06 | Multilingual PV: low-confidence non-EN/DE routed to human; no auto-finalize | Arabic/Hindi subgroup metrics gated | TEST-NFR-06 INJ-072 |
| NFR-07 | Auditability: prompts, model versions, decisions, abstentions exportable | Retirement/inspection scenario sample | TEST-NFR-07 INJ-084 |
| NFR-08 | Degraded mode under OT/MES isolation documented and executable | Runbook steps for INJ-069 | TEST-NFR-08 degraded |

## 4. GxP, safety, security and privacy requirements

### GxP

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| GXP-01 | ALCOA+ originals preserved; no overwrite of source values | Derived views separate; lineage recorded | TEST-GXP-01 integrity |
| GXP-02 | Authority and effective time required on cited policy/evidence | Missing metadata → abstain | TEST-GXP-02 authority |
| GXP-03 | Prohibited autonomous GxP actions impossible via tools | Boundary matrix match E-902 | TEST-GXP-03 hard gate |
| GXP-04 | Validation-state ambiguity surfaced (never assumed validated) | INJ-031 conflict flag | TEST-GXP-04 |
| GXP-05 | Retention/legal hold blocks automated deletion | LH-44 / DSR-17 policy D-204 | TEST-GXP-05 INJ-035 |
| GXP-06 | Human review forced before “ready” acknowledgement when critical deviations exist | INJ-071 omitted fact visible | TEST-GXP-06 bias |

### Safety (PV process controls)

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| GXP-PV-01 | Clock and listedness conflicts preserved for medical review | FR-B-04/05 | TEST-B-04/05 |
| GXP-PV-02 | Signal support remains advisory | No signal confirmation action | TEST-B-08 |

### Security

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| SEC-01 | Entitlements re-checked at execution; stale cache deny-by-default | INJ-067 fixture denies | TEST-SEC-01 |
| SEC-02 | Untrusted knowledge/tools never executed as instructions | Malicious SOP / poisoned manifest inert | TEST-SEC-02 INJ-065/066 |
| SEC-03 | Model artifact hash must match registry or inference blocked | INJ-070 mismatch → fallback | TEST-SEC-03 |
| SEC-04 | Exfiltration attempts on identifiable narratives blocked/logged | INJ-068 pattern | TEST-SEC-04 |
| SEC-05 | Network/tool allowlists honor OT segmentation constraints | Degraded tool set under INJ-069 | TEST-SEC-05 |

### Privacy

| ID | Requirement | Acceptance criteria | Planned test |
|---|---|---|---|
| PRI-01 | Purpose limitation on all workflows | Cross-purpose access denied | TEST-PRI-01 |
| PRI-02 | Sensitive PV segments least-privilege | FR-B-06 | TEST-B-06 |
| PRI-03 | DSR vs GxP retain conflict escalated, not auto-deleted | D-204 / D-401 | TEST-GXP-05 |
| PRI-04 | Residency violations flagged | INJ-064 backup region | TEST-PRI-04 |
| PRI-05 | Secondary use / commercial boundary respected | INJ-060/063 flags | TEST-PRI-05 |

## 5. Acceptance criteria

Cross-cutting definition of done for Phase 5 POC (extends E-901 §9):

1. Workflows A, B and C each have a green deterministic path on golden fixtures including conflict surfacing and abstentions.
2. Zero successful prohibited actions in automated suites (TEST-A-06, TEST-B-08, TEST-C-04).
3. AI-disabled continuity drills pass for all three workflows (TEST-A-07, TEST-B-09, TEST-C-05).
4. Unit, identity, time and authority hard gates pass (TEST-A-03, IDMP/MedDRA flags, timezone tags, SEC-01).
5. Requirements in this matrix are Satisfied, Deferred with waiver ID, or Failed with stop-ship.

## 6. Traceability matrix

| Requirement IDs | Workflow | Architecture / control | Tests | Injects / evidence |
|---|---|---|---|---|
| FR-A-01..07, GXP-01..03,06 | A | ACL LIMS/MES/QMS; RER+C; blueprint A | TEST-A-01..07; TEST-GXP-* | INJ-021..028, 024, 071 |
| FR-B-01..09, GXP-PV-*, PRI-02 | B | Safety ACL; MedDRA/listedness semantics | TEST-B-01..09 | INJ-037..044 |
| FR-C-01..05 | C | Supply ACL; cold-chain association rules | TEST-C-01..05 | INJ-051..058, 080 |
| FR-X-01..05, NFR-01..04,08 | All | Contracts, budgets, offline mode | TEST-X-*; TEST-NFR-* | INJ-082, 076, 069 |
| SEC-01..05 | All | Zero-trust tools; hash pin; authz | TEST-SEC-* | INJ-065..070 |
| PRI-01..05 | All | Purpose bind; retention policy | TEST-PRI-*; TEST-GXP-05 | INJ-035, 059..064 |
| BR-AEGIS-01..05, NFR-05..07 | All | Product governance | BEN-*; GOV-*; TEST-NFR-05..07 | INJ-001..003, 072..074, 084 |
| Domain model | All | Artefacts 05–08; Evidence Map | Design review DR-P2 | INJ-005, 018, 024, 045 |

## 7. Change and waiver control

| Rule | Detail |
|---|---|
| ID stability | Requirement IDs are immutable; wording changes create a new version row with change record |
| Waiver | Only GxP/quality (GxP/SEC) or Security/privacy (PRI/SEC) may waive with written rationale, expiry and compensating control; Product may not waive hard gates |
| Hard-gate non-waiver | Prohibited actions, silent unit conversion, stale-authz allow, and fabrication of missing evidence cannot be waived for scoring |
| Linkage | Code/tests must reference requirement IDs in names or metadata |
| Conflict with injects | Challenge contradictions are not “fixed” by requirement change; they become acceptance scenarios |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|
| R-901 | Assumption | Planned test IDs will be implemented as automated tests in Phase 5 | Traceability gap if skipped | Build / Evaluation | POC gate | Open |
| R-902 | Risk | BR-01 numeric −14% not fully measurable in offline POC | Benefits claim qualitative | Product | BEN-01 design | Open |
| R-903 | Gap | Detailed UI wireframes not requirements-frozen | NFR-05 interpretation variance | Product / Build | Phase 5 | Open |
| R-904 | Risk | Additional clinical/research injects pull scope beyond A–C | Dilution | Product | D-001 enforcement | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Unique FR/NFR/GXP/SEC/PRI IDs for A–C | §§2–4 | ID uniqueness review | This artefact | Accepted |
| Acceptance criteria + planned tests | §§2–5 | Trace matrix §6 | E-901..E-910 | Accepted |
| Hard gates non-waivable | §7; D-206 | Scoring alignment | E-902, E-906 | Accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| GxP/quality lead | GxP | Separate prohibited tests per workflow | TEST-A-06/B-08/C-04 | 2026-08-10 |
| Security/privacy lead | Security | SEC/PRI coverage for injects 065–070 / 035 | §4 tables | 2026-08-10 |
| Evaluation lead | Evaluation | Planned test IDs stable for Phase 5/6 | Confirmed | 2026-08-10 |
