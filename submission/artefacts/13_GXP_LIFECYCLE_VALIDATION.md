# GxP Lifecycle and Validation

> Participant working artefact for Project AEGIS-PHARMA. Cites `knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md` (K-010) and `knowledge/AI_GXP_BOUNDARY.md` (K-003). Training scenario documents — applicability verified for synthetic NTG use only.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — GxP / quality lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Architecture/integration lead; Evaluation/reliability lead; Security/privacy lead |
| Status | Reviewed |
| Related requirements / ADRs | ADR-003, ADR-009; D-002; INJ-006; artefacts 14–15 |

## Purpose

State intended use, GxP boundary and a CSV/CSA proportionate lifecycle approach for AEGIS-PHARMA as an advisory computerised system that must not replace accountable Quality, PV or supply execution decisions.

Accountable owner: GxP / quality lead. Completion criteria: intended use, risk classification, lifecycle deliverables, assurance strategy, supplier/config controls, change/periodic review and retention/retirement are evidence-cited.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-431 | `knowledge/AI_GXP_BOUNDARY.md` (K-003) | NovaCura Global Policy; approved; effective 2026-05-01 | AI may support evidence review; cannot replace accountable GxP decisions; classify by intended use/impact | Synthetic controlled document |
| E-432 | `knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md` (K-010) | NovaCura Global Policy; approved; effective 2026-03-10 | Define intended use, requirements, supplier assessment, risk, acceptance; control config/access/audit/backup/continuity/change/periodic review; preserve through retirement | Synthetic controlled document |
| E-433 | `data/ai_use_boundaries.csv` | Executive prohibition (INJ-006) | Allowed vs prohibited AI actions | Binding for POC |
| E-434 | `case/INTEGRATED_CASE.md` §§3–5 | Case authority | Three workflows; operating properties | Narrative |
| E-435 | `case/STAKEHOLDER_PACK.md` | Stakeholder mandates | QP/PV human-only finals; Quality independence | Deliberate conflicts |

## 1. Intended use and boundary

**Intended use:** AEGIS-PHARMA assists authorized personnel to reconcile and cite evidence, surface contradictions/gaps, abstain under unresolved identity/unit/time/authority, and package human review artefacts for (A) batch-review readiness, (B) PV intake support and (C) supply shortage/cold-chain option drafting — in offline-capable mode for NovaCura Therapeutics Group training/POC scope (E-434).

**Not intended use / GxP boundary (fail closed):** Autonomous or system-issued batch disposition (release/reject/reprocess/recall), final PV seriousness/causality/expectedness/reportability/signal confirmation, clinical eligibility determination, stock reservation/allocation/shipment, or quality-status change (E-431; E-433; E-435).

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Is AEGIS GxP-relevant? | Yes — it influences evidence completeness and review efficiency for regulated processes, even as advisory | GxP | This §1; K-003 |
| Who remains accountable? | Named authorized human roles (QP/QA, Safety physician/PV, Supply governance) | GxP + Stakeholders | E-435 |
| Spec/formulation change? | Out of scope; BR-01 forbids specification/Quality-authority change | Product + GxP | Board BR-01 |

## 2. Risk classification

Proportionate to patient/product/trial integrity impact of **incorrect advisory content that a human might accept**, not of autonomous execution (which is architecturally prohibited).

| Area | Impact if wrong advice accepted | Initial class | Assurance intensity |
|---|---|---|---|
| AuthZ / purpose checks | Unauthorized access to regulated records | High | Scripted + adversarial |
| Evidence integrity / omitted critical deviation | False readiness (INJ-071) | High | Scripted + unscripted exploration |
| Unit conversion | Wrong potency interpretation (INJ-024) | High | Deterministic tests |
| Prohibited action leakage | Regulatory decision by system | High (gated to zero) | Contract fail-closed tests |
| Draft supply ranking | Suboptimal human choice if constraints omitted | Medium | Constraint fixture tests |
| Inference phrasing | Misleading summary | Medium (with forced evidence view) | Unscripted + bias drills |
| Cosmetic UI | Low | Low | Smoke |

Classification follows K-010 risk-based lifecycle and K-003 component classification by impact on product quality, trial integrity, safety and regulated records.

## 3. Lifecycle deliverables

Mapped to K-010 mandatory controls:

| Lifecycle stage | Deliverable under `submission/` | Owner |
|---|---|---|
| Intended use | This artefact §1; blueprint 04 | GxP + Product |
| Requirements | Traceability artefact 09; contracts 12 | Domain + Architecture |
| Supplier assessment | Inference/vendor replaceability ADR-002; no uncontrolled cloud dependency in POC | Security + Architecture |
| Risk & acceptance | Artefacts 14–15; residual risk acceptance | GxP |
| Build & configure | `submission/src/`, fixtures, kill switch, AI-disabled path | Build |
| Verification / assurance | Contract tests; later TEVV | Evaluation |
| Access & audit trail | AuthZ gate; audit export | Security + Evaluation |
| Backup / continuity | Offline package; continuity CSV AI-disabled path | Evaluation |
| Change & periodic review | §6 | GxP |
| Retirement | §7 | Architecture + GxP |

## 4. Validation/assurance strategy

Team 3 applies a **proportionate CSV mindset with CSA critical thinking** (detail in artefact 14):

- High-risk controls (authZ, integrity, units, prohibited fields, human-review forcing) require documented test evidence before defence.
- Lower-risk presentation elements use lighter assurance.
- AI components are assured as **assistive**; decision functions remain outside the validated automated boundary (K-003).
- Offline deterministic mode is the validated continuity configuration; inference is an optional additive path behind budgets and kill switch.

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| CSV vs CSA | Use CSA risk-based methods inside a lifecycle that still produces intended use, risk, acceptance and change evidence per K-010 | GxP | Artefacts 13–14 |
| AI validation stance | Validate controls that bound AI; do not claim validated autonomous GxP decisions | GxP | E-431 |

## 5. Supplier and configuration controls

| Control | Approach |
|---|---|
| Package challenge content | Immutable outside `submission/`; treat as untrusted until authority checked |
| Inference provider | Replaceable adapter; hash pin; kill switch; AI-disabled continuity |
| Configuration | Versioned contracts; deny-by-default entitlements; feature flags for inference |
| Access | Purpose-bound; execution-time re-check |
| Audit | Preserve inputs, transformations, conflicts, gaps, reviewer actions (K-010 evidence expected) |

## 6. Change and periodic review

| Change type | Gate |
|---|---|
| Schema / prohibited field change | Architecture + GxP; contract tests must remain fail-closed |
| New tool registration | Security hash/signature review; write tools denied |
| Inference model change | Hash verification; regression on high-risk fixtures; kill switch ready |
| Workflow scope expansion beyond A–C | Product + GxP veto path |
| Periodic review | Before defence and on inject invalidation of assumptions; confirm intended use unchanged |

## 7. Retention and retirement

| Topic | Rule |
|---|---|
| Retention | Preserve request/response hashes, evidence integrity digests, abstentions, reviewer acknowledgements and audit events for the POC retention window defined in package continuity/privacy constraints |
| Deletion | Never automated against GxP holds (privacy vs retention conflicts escalate to Security + GxP) |
| Retirement | Export final evidence pack; revoke entitlements; disable inference keys; archive contracts/tests; record retirement in decision log per K-010 preserve-through-retirement |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-431 | Assumption | K-003/K-010 synthetic policies are applicable authorities for NTG training scenario within their effective dates | Wrong boundary if superseded | Domain | Superseding knowledge doc | Accepted |
| R-432 | Gap | Full IQ/OQ-style scripts deferred; CSA unscripted evidence planned in build/TEVV phases | Assurance depth | Evaluation | Defence gate | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Intended use bounded | §1 | Contract prohibited-action tests | E-431..E-433 | Design accepted |
| Lifecycle per K-010 | §§3–7 | Review checklist | E-432 | Design accepted |
| AI cannot replace GxP decisions | Boundary §1; ADR-003/009 | Fail-closed tests | `submission/tests/` | Tests green |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Architecture lead | Reviewer | Tie continuity to K-010 backup/continuity control | §3 table row | 2026-08-10 |
| Evaluation lead | Reviewer | Clarify CSA detail lives in artefact 14 | §4 pointer | 2026-08-10 |
| Security lead | Reviewer | Retention vs deletion escalation | §7 | 2026-08-10 |
