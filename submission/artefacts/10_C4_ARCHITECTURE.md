# C4 Architecture

> Participant working artefact for Project AEGIS-PHARMA. Analysis cites challenge evidence under `case/`, `data/`, `knowledge/` and `starter/`; implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Architecture / integration lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | GxP/quality lead; Security/privacy lead; Build lead |
| Status | Reviewed |
| Related requirements / ADRs | D-001..D-004; ADR-001..ADR-012 (`11_ADR_REGISTER.md`); INJ-006, INJ-024, INJ-065..070, INJ-071, INJ-082 |

## Purpose

Define the C4 context, container and component architecture for an offline-capable advisory system that supports the three mandatory workflows (batch evidence reconciliation, PV intake/signal support, supply options/cold-chain recovery) while coexisting with brownfield LIMS/MES/QMS/safety/IRT systems, preserving a kill switch and an AI-disabled continuity path (`case/INTEGRATED_CASE.md` §§3–5; `PACKAGE_SCOPE_AND_ASSUMPTIONS.md`; D-001, D-004).

Accountable owner: Architecture / integration lead. Completion criteria: context/container/component views, trust boundaries, offline/kill-switch paths and acceptance tests are evidence-cited and independently reviewed.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-401 | `case/INTEGRATED_CASE.md` §§2–5 | Case authority for capstone | Three workflows; brownfield fragmentation; operating properties (provenance, abstention, budgets, kill switch) | Narrative; details in CSV injects |
| E-402 | `data/ai_use_boundaries.csv` | Executive prohibition (INJ-006) | Allowed reconcile/cite/flag/abstain; prohibited release/PV final/allocate | Binding hard-gate input |
| E-403 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Package operating assumptions | Offline synthetic mode; participant freedom for architecture | Synthetic training package |
| E-404 | `data/continuity_requirements.csv` | Continuity policy (INJ-082) | Batch/supply 14-day AI-disabled; PV manual required | Synthetic continuity rows |
| E-405 | `starter/contracts/WORKFLOW_CONTRACTS.md` | Starter contract summary | Batch/PV/supply I/O boundaries; no disposition/side effects | Points to `evaluation/contracts/` |
| E-406 | `knowledge/AI_GXP_BOUNDARY.md` (K-003) | NovaCura Global Policy; effective 2026-05-01 | AI supports evidence review; cannot replace accountable GxP decisions | Synthetic controlled document |
| E-407 | `knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md` (K-010) | NovaCura Global Policy; effective 2026-03-10 | Intended use, risk-based lifecycle, continuity, change, retirement | Synthetic controlled document |
| E-408 | `starter/baseline_diagnostics.py` output (preflight) | Diagnostic findings | Stale entitlement, model hash mismatch, unapproved units, untrusted knowledge | Runtime observation on package |

## 1. System context

AEGIS-PHARMA sits beside — not inside — LIMS, MES/eBR, QMS, safety databases and IRT/clinical supply systems. Humans remain the accountable decision makers for disposition, final PV judgements and stock actions (E-402; E-406).

```
[Authorized reviewers: QP / QA / PV / Supply planners]
           |  purpose + entitlement check
           v
    +------------------+
    |  AEGIS-PHARMA    |  advisory only; offline-capable
    |  (Team 3 POC)    |
    +--------+---------+
             | read-only adapters / fixtures (no write tools)
   +---------+---------+---------+----------+
   v         v         v         v          v
 LIMS      MES/eBR    QMS     Safety DB    IRT / inventory
```

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Who uses the system? | Authorized Quality, PV and Supply reviewers with purpose-bound access | Security (D-009) | Entitlement checks at execution time |
| What does it do for them? | Cite evidence, surface contradictions/gaps, abstain, package review readiness and draft supply options | Product (D-001) | Workflow contracts E-405 |
| What does it never do? | Batch disposition, final PV causality/reportability, reserve/allocate/ship/recall, quality-status change | GxP (D-002) | Fail-closed contract tests |
| External systems | LIMS, MES/eBR, QMS, safety, IRT/inventory remain systems of record | Architecture | Brownfield coexistence §2 |
| Trust model | Retrieved docs and tool descriptions are untrusted data until authority/signature/applicability verified | Security (D-008) | INJ-065, INJ-066 |

## 2. Container view

| Container | Responsibility | Technology stance | Data crossing boundary |
|---|---|---|---|
| Advisory API / CLI | Accept versioned requests; enforce authZ, contracts, budgets, kill switch | Stdlib Python under `submission/` | Request/response JSON; audit events |
| Deterministic reconciliation engine | Rules, identity/unit/time checks, contradiction detection | Offline fixtures + rules | Evidence items with integrity hashes |
| Inference adapter (optional) | Replaceable interface for generative assist; never sole path | Behind kill switch and budget | Prompt inputs + structured suggestions only |
| Policy guard | Deny prohibited actions, stale auth, poisoned tools | Fail closed (`policy_guard.py`) | Allow/deny decisions |
| Evidence & audit store | Preserve source facts, abstentions, reviewer actions | Local submission evidence export | Append-only audit records |
| Human review workbench | Forced evidence view; acknowledge gaps before “ready” | UI or CLI checklist | Review acknowledgements |
| Brownfield read adapters | Map LIMS/MES/QMS/safety/IRT snapshots to evidence items | Fixture-backed in POC | Read-only snapshots; no write-back |

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Why separate inference adapter? | Model hash mismatch (INJ-070) must not block advisory work; AI-disabled path required (E-404) | Architecture (ADR-002) | Kill switch + offline demo |
| Why no write container? | Poisoned write tools (INJ-066) and AI-use boundaries forbid side effects | Security + GxP | Tool catalog deny writes |
| How do brownfield systems coexist? | AEGIS consumes exports/fixtures; systems of record retain authority for status changes | Architecture | Context diagram §1 |

## 3. Component view

Shared components across Workflows A–C:

| Component | Function | Fail-closed behaviour |
|---|---|---|
| AuthZ gate | Re-check user, purpose, object, role, tool at execution time | Deny on stale/ambiguous entitlement (INJ-067) |
| Contract validator | Versioned schemas; `additionalProperties: false` | Reject prohibited fields |
| Authority & retrieval gate | Verify status, authority, effective date, hash/signature, applicability | Abstain / escalate if unresolved |
| Unit & identity resolver | Approved mapping only (INJ-024) | Abstain; never silent convert |
| Contradiction engine | Preserve conflicting evidence; never “clean” silently | Surface conflict; readiness = conflicted/insufficient |
| Review packager | Build human_review payload with forced critical-deviation list (INJ-071) | Block “ready” without acknowledgement |
| Budget & stop controller | Token/step/cost budgets; checkpoints; rollback | Stop and degrade to deterministic path |
| Kill switch | Disables inference adapter globally | Continuity via AI-disabled path |
| Audit exporter | Hash-linked event trail | Refuse to drop conflicting evidence |

Workflow-specific components:

| Workflow | Components | Output stance |
|---|---|---|
| A — batch_evidence | Genealogy/unit comparators; applicable-document selector; readiness_state | No disposition property |
| B — pv_intake | Source-fact preserver; duplicate candidate scorer; clock reconstructor; listedness context | No final causality/reportability |
| C — supply_options | Constraint enumerator; draft option ranker; quality-hold surfacer | `no_side_effects: true` only |

## 4. Critical code/sequence view

Happy path (deterministic, AI off or kill switch engaged):

1. Receive request with `request_id`, purpose, as-of, user context and idempotency key.
2. AuthZ gate re-checks entitlement; deny → audit and stop.
3. Load fixtures/adapters; validate authority and integrity per evidence item.
4. Run deterministic reconciliation; record contradictions, gaps, abstentions.
5. Package human_review; set `execution_status: not_executed`.
6. Validate response against versioned schema; emit audit.

Optional inference path (AI on, budgets remaining, kill switch open):

1. After step 4, call Inference adapter for suggestion text only.
2. Merge suggestions as non-authoritative annotations; never overwrite source facts.
3. On budget exhaustion, hash mismatch or kill switch → discard inference, continue from deterministic result.

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Where does kill switch act? | Between deterministic engine and inference adapter only | Architecture (ADR-011) | Continuity drill |
| Where do prohibited fields fail? | Contract validator and policy guard before any export/UI handoff | Build | `submission/tests/test_workflow_contracts.py` |
| Idempotency | Same idempotency key + same payload → same response hash; no duplicate side effects (none exist) | Architecture (ADR-007) | Contract §6 |

## 5. Trust and GxP boundaries

| Boundary | Inside AEGIS | Outside AEGIS (human / SoR) |
|---|---|---|
| Evidence reconciliation | Cite, flag, abstain, package | Disposition / batch release |
| PV support | Intake packaging, duplicate candidates, clock evidence | Final seriousness/causality/expectedness/reportability/signal confirmation |
| Supply support | Draft options, violated constraints, approvals list | Reserve, allocate, ship, recall, quality-status change |
| Validation | CSA/CSV proportionate assurance for advisory controls | Regulated decision accountability (K-003) |

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| GxP relevance | Advisory computerised system affecting review efficiency and evidence integrity; decisions remain human (E-406, E-407) | GxP | Artefacts 13–15 |
| Untrusted content | Knowledge corpus and tool manifests treated as data | Security (D-008) | Authority gate |
| Automation bias control | Forced evidence view before readiness acknowledgement (INJ-071) | GxP | Blueprint §4 |

## 6. Data and event flows

| Flow | Direction | Semantics |
|---|---|---|
| Request accepted | Inbound | Versioned; purpose-bound; idempotency key required |
| Evidence retrieved | Inbound (read) | Preserve source, authority, effective time, unit, verbatim value, uncertainty |
| Advisory response | Outbound | Schema-valid; `execution_status: not_executed` |
| Audit event | Outbound/append | Who/what/when/purpose/decision/evidence hashes |
| Kill-switch event | Control plane | Inference disabled; continuity path activated |
| Review acknowledgement | Inbound human | Recorded before readiness promotion |

Events are advisory notifications and audit records only — never inventory or quality-status commands.

## 7. Deployment and offline mode

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| POC deployment | Local/offline under `submission/`; no cloud keys required | Build (A-003) | Preflight + offline demo |
| AI-disabled path | Rules + fixtures for all three workflows; PV manual forms where required (E-404) | Evaluation | Continuity runbook |
| Kill switch | Config/env flag disables inference adapter; deterministic path remains | Architecture (ADR-011) | Outage drill |
| Brownfield | Fixture snapshots stand in for LIMS/MES/QMS/safety/IRT in POC | Architecture | Contract samples |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-401 | Assumption | Fixture snapshots adequately represent brownfield read interfaces for POC defence | Demo may understate adapter variance | Architecture | Live adapter spike | Open |
| R-402 | Risk | Reviewers skip forced evidence view under schedule pressure (INJ-002, INJ-071) | Automation bias | GxP | UI acknowledgement test | Open |
| R-403 | Gap | Live brownfield connectivity remains design-only for workshop POC | Production cutover incomplete | Architecture | Post-defence | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Offline three-workflow advisory | Containers §2–3 | Offline demo + contract tests | `submission/tests/` | Design accepted |
| No prohibited actions | Fail-closed validator + policy guard | Positive/negative contract tests | `evaluation/contracts/` + fixtures | Tests green |
| Kill switch / AI-disabled | §4, §7 | Continuity requirements E-404 | Assumptions A-009 | Design accepted |
| Brownfield coexistence | Context §1 | No write tools in catalog | INJ-066 stance | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| GxP/quality lead | Reviewer | Emphasize K-003 boundary in context diagram | Added §5 table citing E-406 | 2026-08-10 |
| Security/privacy lead | Reviewer | Require kill switch on inference only, not whole advisory path | Clarified §4 sequence | 2026-08-10 |
| Build lead | Reviewer | Point acceptance to contract tests under submission | Traceability updated | 2026-08-10 |

---

## Prompt 09 / 10 structural reopen gate (2026-08-11)

| Field | Entry |
|---|---|
| Decision | **cleared** |
| Reopen of artefacts 06–08 / C4 | **Not required** — no waste-driven container or context change from thin DMAIC notes |
| Residual | Full Prompt 09 DOWNTIME workshop still pending; does **not** block Prompt 10/11 assessment build |
| Recorded for | `submission/prompts/10_implementation_tasks.md` entry/exit |
