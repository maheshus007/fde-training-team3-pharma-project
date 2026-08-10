# Product and Service Blueprint

> Participant working artefact describing the AEGIS-PHARMA product/service experience for NovaCura’s three mandatory workflows.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product / value lead with Build lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | GxP/quality lead; Evaluation/reliability lead; Security/privacy lead |
| Status | Reviewed |
| Related requirements / ADRs | `case/INTEGRATED_CASE.md` §4–5; INJ-001..006; `data/ai_use_boundaries.csv`; D-001..D-005 |

## Purpose

Define personas, intended/prohibited uses, frontstage/backstage flows, human review, failure/recovery, accessibility and success measures for an offline-capable AEGIS service that assists — never replaces — regulated decision makers.

Accountable owner: Product/value lead. Completion criteria: each workflow has a blueprint path including AI-disabled continuity and explicit prohibitions.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-301 | `case/INTEGRATED_CASE.md` §4–5 | Case | Workflow A–C scope and operating properties | Narrative |
| E-302 | `data/ai_use_boundaries.csv` | INJ-006 | Allowed vs prohibited per use case | Binding |
| E-303 | `case/STAKEHOLDER_PACK.md` | Stakeholder pack | User mandates and concerns | Qualitative |
| E-304 | `data/no_ai_baselines.csv` | INJ-003 | Non-AI alternatives | Estimates |
| E-305 | `data/kpi_conflicts.csv` | INJ-002 | Conflicting success metrics | Targets only |
| E-306 | `data/continuity_requirements.csv` | INJ-082 | Outage tolerances | Synthetic |
| E-307 | `data/board_requests.csv` BR-01 | Board | Lead-time goal with Quality constraint | Synthetic |
| E-308 | `data/usability_findings.csv` (INJ-073) | Usability inject | Keyboard/colour-only failure risk | Challenge condition |
| E-309 | Preflight diagnostics | 2026-08-10 | Trust/authz/unit defects | Partial |

## 1. Personas and jobs-to-be-done

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Persona Q — Batch evidence reviewer / QP support | Job: assemble complete, cited release-packet evidence under genealogy, EM, OOS and supplier gaps (INJ-021..028). Outcome: readiness assessment with gaps — not certification | Product | E-301, E-303 |
| Persona S — PV intake specialist | Job: intake, duplicate cluster, terminology/version flags, clock reconstruction, listedness source conflict surfacing (INJ-037..044). Outcome: human-ready case file — not causality/seriousness | Product | E-301, E-302 |
| Persona P — Supply planner | Job: generate traceable shortage/cold-chain options under quality status, MA, trial/compassionate constraints (INJ-051..058). Outcome: ranked options — not allocation/shipment | Product | E-301, E-302 |
| Persona C — Control reviewer (Quality/Security) | Job: verify abstentions, entitlement denials, untrusted knowledge handling | Security/GxP | E-309 |

## 2. Intended and prohibited uses

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Intended — batch | reconcile, cite, flag, abstain (E-302) | GxP | Boundary tests |
| Prohibited — batch | release / reject / reprocess / recall | GxP | Hard gate |
| Intended — PV | extract, normalize, cluster, cite | PV governance | Boundary tests |
| Prohibited — PV | final causality / seriousness / reportability (and signal confirmation per case §4) | PV governance | Hard gate |
| Intended — supply | generate options | Supply + Quality | Boundary tests |
| Prohibited — supply | reserve / allocate / ship (and recall initiation per case §4) | Supply + Quality | Hard gate |
| Cross-cutting prohibition | No autonomous formulation, specification, clinical eligibility changes (INJ-006) | GxP | E-302 |

## 3. Frontstage/backstage workflow

### Workflow A — GxP evidence reconciliation (batch-review readiness)

| Stage | Frontstage (user) | Backstage (system) |
|---|---|---|
| Intake | Select batch / packet ID; state purpose “review readiness” | Bind user, role, purpose; load entitlements at execution time |
| Gather | See source list with authority and effective time | Query MES/LIMS/QMS/EM/supplier fixtures; preserve contradictions |
| Reconcile | View gap/contradiction board (genealogy break INJ-021, unit issue INJ-024, etc.) | Deterministic compare; abstain on unapproved unit maps |
| Review | Human confirms evidence pack; may escalate | No disposition write path exists |
| AI-disabled | Same screens using rules and cached fixtures only | Model inference off; runbook E-306 |

### Workflow B — PV case-intake and signal-support

| Stage | Frontstage | Backstage |
|---|---|---|
| Intake | Paste/import case narrative (multilingual) | Segment sensitive fields (INJ-041); purpose bind |
| Normalize | See coding candidates with MedDRA version labels | Flag version mismatch (INJ-039); do not auto-merge duplicates |
| Cluster | Review duplicate candidates (INJ-037) | Cluster with citations; human merge only outside prohibited auto-disposition |
| Clock / listedness | See awareness-date conflict and label/IB/CDS divergence | Reconstruct timeline; abstain on authenticity failures (INJ-042) |
| AI-disabled | Manual forms + rules extractors | Meets PV manual requirement (E-306) |

### Workflow C — Supply shortage / cold-chain recovery planner

| Stage | Frontstage | Backstage |
|---|---|---|
| Situation | Enter shortage or excursion case | Load inventory, quality status, MA, constraints (INJ-054..056) |
| Options | Browse traceable options with constraints and ethics flags | Generate options only; no reserve/allocate tools registered |
| Cold-chain | Inspect logger/pallet disputes (INJ-051) | Preserve clock disputes; abstain if association unresolved |
| Handoff | Export option pack for human planning approval | Audit trail of recommendations |
| AI-disabled | Spreadsheet/rules option enumerator per runbook | 14-day continuity (E-306) |

Backstage shared services: evidence store under `submission/`, contract validation, budget/kill switch, audit export, offline package mode (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md`).

## 4. Human review touchpoints

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Mandatory gates | Disposition (human QP/Quality systems); final PV judgements; allocation/shipment/recall approvals | GxP | E-302, E-303 |
| Forced evidence view | Before acknowledging a “ready” summary, reviewer must see critical deviation list to counter automation bias (INJ-071) | GxP | Candidate output tests later |
| Sensitive data | Pregnancy/paediatric segments require elevated role (INJ-041) | Security/Privacy | Access tests |
| Untrusted content | Supplier PDFs shown as data; hidden instructions never executed (INJ-065) | Security | Red-team fixtures |
| Local confirmation | Site/local facts can reject central suggestions (stakeholder pack) | Domain | Blueprint acceptance |

## 5. Failure and recovery journey

| Failure | User experience | Recovery |
|---|---|---|
| Stale entitlement (INJ-067) | Action denied with reason | Re-authz; no cache override |
| Model hash mismatch (INJ-070) | Inference blocked | Fall back to deterministic/AI-disabled path |
| Unapproved unit mapping (INJ-024) | Field marked abstain | Human/lab resolves mapping under change control |
| Untrusted knowledge (INJ-065) | Warning; content not actionable as policy | Security review of source |
| Region AI outage (INJ-079) | Banner: AI disabled | Continuity runbook; E-306 windows |
| Checkpoint corruption (INJ-080) | Resume rejected if state stale | Restart from last verified checkpoint; no draft reservations |
| Ransomware / OT isolation (INJ-069) | Degraded MES/QMS mode | Manual evidence collection procedures |

## 6. Accessibility and multilingual experience

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Accessibility | Challenge usability finding: cannot operate fully by keyboard; colour-only warnings (INJ-073 / E-308). AEGIS UI requirements: full keyboard path, text+icon status, sufficient contrast | Product + Build | Usability tests |
| Multilingual PV | Arabic/Hindi extraction quality risk vs EN/DE (INJ-072) | Evaluation | Subgroup metrics; abstain/low-confidence routing to human |
| Language equity control | Never auto-finalize non-English cases on low confidence | PV governance | Performance gates |
| Patient Safety Representative concern | Transparency and contestability of AI outputs (E-303) | Product | Show sources and abstention reasons |

## 7. Success measures

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Board-aligned | Contribution to −14% release lead time without Quality-authority change (E-307) | Product | Benefits plan |
| Workflow quality | Gap detection recall on fixture packs; citation completeness; zero prohibited actions | Evaluation | Hard gates + scorecard |
| No-AI fairness | Publish comparison vs master_data_repair and rules_workflow (E-304) | Product | INJ-003 response |
| Guardrails | Entitlement deny correctness; AI-disabled task success; review minutes included (INJ-077); token/cost within budget | Evaluation + Security | FinOps/reliability artefacts |
| Conflict honesty | Do not claim success if Quality RFT or Safety expedited metrics were sacrificed invisibly (E-305) | Product/GxP | Stakeholder review |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-301 | Risk | UI ships with colour-only warnings despite INJ-073 | Accessibility hard fail | Build | UI acceptance | Open |
| R-302 | Risk | Multilingual gap ignored | Inequitable PV support | Evaluation | Subgroup gate | Open |
| R-303 | Assumption | Offline demonstrator UX sufficient for defence | Examiner expects richer integration | Product | Defence artefact 30 | Open |
| R-304 | Gap | Detailed screen wireframes deferred to build phase | Ambiguity for Build | Product | Phase 5 POC | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Three workflows with human-only finals | No write tools for prohibited actions | Prohibited-action suite | E-301, E-302 | Design accepted |
| AI-disabled continuity | Dual-path blueprint | Outage drills | E-306 | Design accepted |
| Accessibility and language controls | UI + confidence routing | Usability + subgroup eval | E-308; INJ-072 | Requirements accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| GxP/quality lead | Reviewer | Require forced evidence view against INJ-071 | Added §4 | 2026-08-10 |
| Evaluation/reliability lead | Reviewer | Require continuity rows per workflow | Added §3 AI-disabled rows | 2026-08-10 |
| Security/privacy lead | Reviewer | Untrusted PDF handling explicit | Added §4/§5 | 2026-08-10 |
