# Computer Software Assurance

> Participant working artefact for Project AEGIS-PHARMA. Applies risk-based CSA critical thinking proportionate to the advisory intended use in `13_GXP_LIFECYCLE_VALIDATION.md` and K-003/K-010.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — GxP / quality lead with Evaluation/reliability lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Architecture/integration lead; Security/privacy lead; Build lead |
| Status | Reviewed |
| Related requirements / ADRs | Artefact 13; ADR-003, ADR-007, ADR-009, ADR-010; INJ-024, INJ-071 |

## Purpose

Define risk-based computer software assurance for AEGIS-PHARMA: focus assurance effort on high-risk functions, apply critical thinking, and use unscripted testing where it better reveals automation-bias and omitted-evidence failures than rote scripted scripts alone.

Accountable owner: GxP / quality lead. Completion criteria: high-risk inventory, assurance methods, scripted/unscripted mix, defect handling, release evidence and continuous assurance triggers.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-441 | `knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md` (K-010) | Effective 2026-03-10 | Risk-based validation/assurance; evidence of conflicts, gaps, reviewer actions | Synthetic |
| E-442 | `knowledge/AI_GXP_BOUNDARY.md` (K-003) | Effective 2026-05-01 | Assure controls proportionate to risk; reserve decisions to authorized roles | Synthetic |
| E-443 | `evaluation/contracts/*.schema.json` | Package schemas | Fail-closed structural controls | Executable |
| E-444 | `case/INTEGRATED_CASE.md` INJ-071, INJ-024 | Case injects | Automation bias; unit conversion hazard | Narrative + data |
| E-445 | `tools/test_contracts.py` | Package pattern | Positive/negative contract proof pattern | Immutable tool |

## 1. Critical thinking and risk basis

Assurance questions (CSA posture):

1. What is the intended use and what patient/product/record harm follows if the software is wrong?
2. Which features are decision-adjacent (influence humans) versus decorative?
3. Which failures are already mitigated by architecture (no write tools, schema denial)?
4. Where would scripted tests give false confidence (reviewer behaviour, omitted evidence)?

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Effort focus | AuthZ, evidence integrity, units, prohibited fields, human-review forcing, continuity | GxP + Evaluation | §2 |
| Effort de-emphasize | Theme colours, non-decision copy edits | Product | Low-risk class in artefact 13 |

## 2. High-risk functions

| ID | Function | Harm if fails | Architecture mitigator | Assurance |
|---|---|---|---|---|
| HR-01 | Entitlement re-check | Unauthorized regulated data use | Deny-by-default (ADR-012) | Scripted stale-cache cases |
| HR-02 | Prohibited field rejection | System appears to decide disposition/causality/side effects | Schema `additionalProperties: false` | Contract negatives |
| HR-03 | Unit mapping gate | Wrong strength interpretation | Abstain without approved map | Deterministic unit fixtures |
| HR-04 | Critical deviation surfacing | Automation bias / omitted evidence (INJ-071) | Forced evidence view | Unscripted review drills |
| HR-05 | Authority-checked citation | Citing superseded/untrusted docs | Authority gate (ADR-004) | Adversarial retrieval fixtures |
| HR-06 | Supply no-side-effects | Apparent reservation/allocation | `no_side_effects` const | Contract negatives |
| HR-07 | Kill switch / AI-disabled path | Loss of continuity or unsafe AI-only path | ADR-011 | Outage drill |
| HR-08 | Budget/stop | Incomplete AI answer presented as complete | ADR-010 | Stop-injection tests |

## 3. Assurance methods

| Method | When used |
|---|---|
| Deterministic unit/contract tests | Structural fail-closed rules; unit conversion gates |
| Scripted scenario tests | Known injects (genealogy break, duplicate PV, shortage constraints) |
| Unscripted exploratory testing | Reviewer journeys hunting omitted deviations and misleading summaries |
| Adversarial / red-team | Poisoned tools, untrusted docs, stale entitlements |
| Continuity drills | AI-disabled and kill-switch operation |
| Traceability review | Requirement → control → test → evidence path |

## 4. Unscripted and scripted evidence

| Risk area | Scripted | Unscripted (appropriate) |
|---|---|---|
| Schema prohibited fields | Yes — `test_workflow_contracts.py` | Optional fuzz of additional keys |
| Unit conversion (INJ-024) | Yes — approved vs unapproved maps | Explorer tries ambiguous unit labels |
| Automation bias (INJ-071) | Checklist that critical deviations appear in payload | Reviewer performs timed review; observer notes skipped evidence |
| Multilingual PV | Fixture golden paths | Explorer uses unexpected language mixes |
| UI layout | Smoke | Exploratory usability/accessibility |

Unscripted testing is preferred for human-factor and omitted-evidence risks because scripted “click acknowledge” tests can pass while real reviewers still skip content.

## 5. Defect handling

| Severity | Examples | Disposition |
|---|---|---|
| Critical | Prohibited field accepted; silent unit convert; write tool callable | Block release; fail closed; root cause before defence |
| Major | Critical deviation omitted from forced list; stale entitlement allow | Block AI-enabled demo; AI-disabled may proceed if unaffected |
| Minor | Wording clarity; non-decision UX | Log; fix in backlog |
| Enhancement | Ranking aesthetics | No assurance gate |

Defects that touch K-003 decision boundary are never waived by Build alone (charter independent review).

## 6. Release decision evidence

Before Phase 3 exit / later defence gates, Evaluation must see:

| Evidence | Source |
|---|---|
| Contract positive/negative results | `submission/scripts/test.py` output |
| Intended use & boundary | Artefact 13 |
| High-risk assurance map | This artefact §§2–4 |
| Residual risk acceptance | Artefact 15 |
| Continuity design | ADR-008/011; continuity CSV |

## 7. Continuous assurance

| Trigger | Action |
|---|---|
| Schema or ADR change | Re-run contract and high-risk suites |
| New inject invalidating assumption | Update QRM; add test |
| Model/tool hash change | Block inference; re-assure adapter |
| Failed kill-switch drill | Treat as major defect |
| Periodic review | Confirm CSA effort still matches risk classification |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-441 | Assumption | Unscripted sessions can be evidenced via observer notes + exported payloads in workshop time | Thin human-factor evidence | Evaluation | Defence scheduling | Open |
| R-442 | Risk | Over-reliance on schema tests misses semantic omission | False confidence | GxP | HR-04 unscripted | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Risk-based CSA | §§1–3 | High-risk map | E-441, E-442 | Design accepted |
| Unscripted where appropriate | §4 | INJ-071 drills | E-444 | Design accepted for method |
| Fail-closed structural assurance | HR-02/HR-06 | unittest | `submission/tests/` | Tests green |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Architecture lead | Reviewer | Map HR items to ADRs | §2 mitigators column | 2026-08-10 |
| Security lead | Reviewer | Include adversarial method | §3 | 2026-08-10 |
| Build lead | Reviewer | Keep Phase 3 gate on contract tests concrete | §6 | 2026-08-10 |
