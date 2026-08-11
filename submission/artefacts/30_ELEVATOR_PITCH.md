# Elevator Pitch and Defence

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v0.1 draft — 2026-08-07 |
| Reviewers | Pending team review |
| Status | Draft |
| Related requirements / ADRs | All artefacts 01–29; submission evidence JSON |

## Purpose

Provides the 60-second pitch, five-minute narrative, and the explicit decision we ask leadership to make — grounded in evidence, with residual risk stated. Accountable owner: capstone team. Completion criteria: pitch does not claim production AI readiness.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-3001 | `01_BUSINESS_CASE.md` | Prior | Lead-time / evidence-hunt problem; AI only after non-AI options | Problem frame |
| E-3002 | `14_COMPUTER_SOFTWARE_ASSURANCE.md` / `28_PRODUCTION_READINESS.md` | Prior | No AI pilot GO | Hard boundary |
| E-3003 | `submission/evidence/{test,evaluation,run}_*.json` | Runs | 51 tests pass; 11/15 fixtures pass; 4 NI honest; workflows schema-safe | POC proof |
| E-3004 | Challenge injects (e.g. SEC-1/2, GXP-SUM-1, QR-11, DSR-17, DT-2) | Challenge data | Failures are real in the estate, not hypothetical | Credibility |

## 1. 60-second pitch

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Pitch | NovaCura’s batch, PV and supply teams lose time to contradictory brownfield evidence — and the AI platform meant to help is itself unvalidated: summariser hash mismatch, unblocked exfiltration/DoW patterns, stale entitlements, open AI outage. We built a **fail-closed, deterministic support layer** that reconciles and cites evidence, clusters PV duplicates, drafts non-executing supply options, and **refuses** compromised models, revoked users, oversized loops and ambiguous deletions. Tests pass; we are **not** asking to turn AI inference on. We are asking to fund remediation to the NO-GO checklist before any supervised pilot. | Capstone team | E-3001–E-3004 |

## 2. Five-minute executive narrative

| Beat | Content |
|---|---|
| 1. Problem | Evidence lead time and release risk driven by genealogy conflicts, missing packet items, open deviations — not lack of a chatbot (artefact 01–02). |
| 2. Estate truth | AI-EVIDENCE failed validation tests; GXP-SUM-1 integrity broken; SEC-1/2 were not blocked; contractor cache stale >2 days; DT-2 still open. |
| 3. Intervention | Three bounded workflows + gateway/gates; schemas forbid side effects; offline mode is default. |
| 4. Proof | 51 unit tests; contract tests; 11 public fixtures gated; 4 gaps labelled `not_implemented` rather than faked. |
| 5. Ask | Accept NO-GO for pilot; approve 90-day P0 remediation (integrity, residency/consent, runbooks, tool allow-list); keep deterministic assist in controlled demo use. |

## 3. Problem and measurable impact

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Problem | Conflicted/incomplete batch evidence and fragmented PV/supply signals in a brownfield estate. | Capstone team | E-3001 |
| Impact of *wrong* AI | Automation bias already accepted an unsafe candidate in 19 seconds; disposition-capable poisoned tool exists in catalogue. | CQO / CISO | Artefacts 16/18 |
| Impact of *our* POC | Surfaces contradictions/gaps; blocks known abuse patterns; does not accelerate false certification. | Capstone team | E-3003 |

## 4. Bounded intervention

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| In | reconcile/cite/flag/abstain; extract/normalize/cluster/cite; draft options only | Capstone team | ai_use_boundaries |
| Out | release, final PV decisions, reserve/allocate/ship, recall initiation, training on withdrawn biomarker data | Capstone team | Artefacts 04/17 |

## 5. Strongest control boundary

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Strongest boundary | Fail closed: no verified model → no inference; revoked IAM → deny despite cache; unknown hold link → abstain deletion; outputs cannot carry disposition language or side effects. | Capstone team | E-3003; src gates |

## 6. Evidence and residual risk

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Evidence | Artefacts 01–29; evidence JSON; challenge CSVs cited throughout. | Capstone team | E-3003, E-3004 |
| Residual risk | Human over-trust without UI; OT ransomware path; residency still violated in estate; vendor concentration; 4 fixtures unimplemented; validation still failed. | CQO | Artefact 28 |

## 7. Decision requested

| Decision | Options | Recommendation |
|---|---|---|
| Supervised AI inference pilot | GO / NO-GO | **NO-GO** (E-3002) |
| Continue deterministic fail-closed assist for defence/training use | Approve / Reject | **Approve** |
| Fund 90-day P0 remediation backlog | Approve / Defer | **Approve** (artefact 29) |
| Next checkpoint | Date TBD | Re-open pilot only when artefact 28 §7 is fully green |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-3001 | Risk | Pitch diluted into “AI is ready” in executive retelling | High | Capstone team | Defence rehearsal | Open |
| R-3002 | Gap | Team member names still pending (A-001) | Low | Capstone team | Before formal sign-off | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Pitch matches assurance case | Artefacts 21/28/30 aligned | Review | E-3002, E-3003 | PASS (doc) |
| Decision request explicit | §7 | Leadership | — | Pending |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | Executive sponsor / CQO | — | — | — |
