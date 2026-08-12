# Token Efficiency and AI FinOps

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v0.1 draft — 2026-08-07 |
| Reviewers | Pending team review |
| Status | Draft |
| Related requirements / ADRs | INJ-075, INJ-076, INJ-077, INJ-078; artefact 16 §6 |

## Purpose

Baselines token/cost reality from challenge data, shows why denial-of-wallet and price-shock matter, and sets POC FinOps rules (budgets, avoided inference, human-review cost visibility). Accountable owner: FinOps / platform owner (role-played). Completion criteria: cost-per-successful-task formula stated; PUB-14 remains not_implemented until a calculator exists in code.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2301 | `data/model_usage.csv` | Usage log, undated | batch_review: 1900 req, 5.8M in / 0.85M out, **1110** successful; pv_intake: 4200 req, 9.2M in / 1.7M out, **2800** successful | Success ≠ request count |
| E-2302 | `data/model_costs.csv` | Price card | AIVENDOR-X large-1: input $8.50/M (was $5.00), output $22/M; LOCAL-SLM small-7b: $0.80/$1.20 | INJ-075 price shock on large-1 |
| E-2303 | `data/cost_model.csv` | Monthly cost model | inference $184,000; observability $31,000; human_quality_review $0; medical_review $0 | INJ-077 — human review cost hidden (zeroed) |
| E-2304 | `data/staff_rates.csv` | Loaded rates | Quality reviewer $92/h; safety physician $165/h; regulatory strategist $148/h | For true cost rebuild |
| E-2305 | `data/security_events.csv` SEC-2 | Security log | 980,000-token loop, blocked=no | INJ-076 DoW |
| E-2306 | `data/vendor_dependencies.csv` | Dependency map | model hosting, vector, evaluation, observability all AIVENDOR-X | INJ-078 concentration |
| E-2307 | `data/model_endpoints.csv` | Endpoints | primary_large EU-West **down**; fallback_small OnPrem-DE available (small-7b) | Routing/cost implication |

## 1. Workload baseline

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Observed volume | E-2301: ~6.1k requests across batch+PV with ~3.9k successful tasks. | Capstone team | E-2301 |
| Success rate | batch 1110/1900 ≈ 58%; PV 2800/4200 ≈ 67% — FinOps must cost **successful** tasks, not raw requests. | FinOps | E-2301 |

## 2. Model/routing strategy

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Price shock | large-1 input price rose 5.00→8.50 (E-2302). | FinOps | E-2302 |
| Current estate routing | Primary large endpoint down; on-prem small available (E-2307). | Platform | E-2307 |
| POC decision | Prefer avoided inference (deterministic workflows) first; any future inference must pass integrity gateway then prefer LOCAL-SLM when within validated scope; never silent fallback to unverified large model. | Capstone team | E-2302, E-2307; ADR-006 |

## 3. Context and token budgets

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Hard cap | `MAX_TOKENS_PER_REQUEST = 50000` denies SEC-2-scale loops (E-2305). | Capstone team | `security_gates.py` |
| Gap | No cumulative monthly token budget / cost-per-task calculator yet (PUB-14 deep path). Suite S11 + `latency_cost_grader` enforce per-request budgets in the TEVV harness. | Capstone team | Gap R-2301; `submission/evaluation/datasets/S11_latency_token_cost_dow.json` |

## 4. Caching and avoided inference

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Avoided inference | Entire assessed mode runs without model calls — workflows are deterministic. This is the primary FinOps control. | Capstone team | `submission/src/workflow_*.py` |
| Cache caution | Entitlement/consent caches already caused safety/privacy failures — cost caching must not reuse those anti-patterns for authz. | Capstone team | Artefacts 12/17 |

## 5. Human-review and validation cost

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Hidden cost | cost_model sets human_quality_review and medical_review to **$0** (E-2303) while staff rates exist (E-2304) — true TCO understated. | FinOps | E-2303, E-2304 |
| Decision | Any business case update must include reviewer minutes × loaded rate; automation-bias accepts are not “savings.” | Capstone team | Artefact 18; E-2304 |

## 6. Cost per successful task

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Formula | `(inference_tokens_cost + allocated_observability + human_review_loaded_cost) / successful_tasks` | FinOps | E-2301–E-2304 |
| Illustrative inference-only (batch, large-1 current prices, ignoring output mix detail) | Using E-2301 token totals × E-2302 rates is directionally high-six-figures monthly when combined with E-2303’s $184k inference line — exact per-task figure requires join of token mix to price that PUB-14 code would compute. **Not fabricated here as a precise USD.** | FinOps | Gap R-2301 |
| POC actual | Deterministic path ≈ $0 inference; residual cost is human review time only. | Capstone team | This build |

## 7. Budget alerts and vendor shock

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Alerts needed | Per-request cap (done); daily/monthly wallet; price-change trigger (E-2302); vendor concentration alert (E-2306). | FinOps | E-2302, E-2305, E-2306 |
| Concentration | Four critical capabilities on one vendor (E-2306) — exit/FinOps coupled (artefact 27). | Procurement | E-2306 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2301 | Gap | No executable cost-per-successful-task calculator (PUB-14 not_implemented) | Medium | Capstone team | Code gap backlog | Open |
| R-2302 | Risk | Business case using $0 human review (E-2303) will overstate AI ROI | High | Capstone team | Update artefact 01 if revised | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Per-request DoW denied | token budget gate | test_security_gates | E-2305 | PASS |
| Cost/task model in code | finops module | PUB-14 | — | not_implemented |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | FinOps | — | — | — |
