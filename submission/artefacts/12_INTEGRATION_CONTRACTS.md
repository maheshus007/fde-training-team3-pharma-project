# Integration Contracts

> Participant working artefact for Project AEGIS-PHARMA. Executable schemas live in `evaluation/contracts/`; Team 3 mirrors fixtures under `submission/tests/fixtures/` and validates via `submission/src/contracts.py`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Architecture / integration lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Build lead; Domain/evidence lead; Evaluation/reliability lead |
| Status | Reviewed |
| Related requirements / ADRs | ADR-003, ADR-006, ADR-007; `starter/contracts/WORKFLOW_CONTRACTS.md`; INJ-006, INJ-024 |

## Purpose

Define versioned I/O contracts, event semantics and idempotency keys for the three workflows, aligned with `starter/contracts/WORKFLOW_CONTRACTS.md` and `evaluation/contracts/`, so positive examples validate and prohibited disposition/causality/side-effect fields fail closed.

Accountable owner: Architecture / integration lead. Completion criteria: inventory, input/output contracts, units/time/identity rules, idempotency and automated contract tests.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-421 | `starter/contracts/WORKFLOW_CONTRACTS.md` | Starter contract summary | Batch/PV/supply I/O; no disposition/side effects | Narrative pointer |
| E-422 | `evaluation/contracts/batch_response.schema.json` | Executable schema | Required fields; `additionalProperties: false`; no disposition | Package-owned |
| E-423 | `evaluation/contracts/pv_response.schema.json` | Executable schema | PV required fields; no final conclusions | Package-owned |
| E-424 | `evaluation/contracts/supply_response.schema.json` | Executable schema | `no_side_effects` const true; options draft | Package-owned |
| E-425 | `evaluation/contracts/evidence_item.schema.json` | Executable schema | Source/authority/integrity/sha256 | Package-owned |
| E-426 | `tools/test_contracts.py` | Package test pattern | Positive pass / negative fail | Challenge tool (immutable) |

## 1. System/interface inventory

| Interface | Direction | Protocol (POC) | Contract version | Owner |
|---|---|---|---|---|
| Batch evidence request/response | In/Out | JSON file/CLI | `batch_response` v1 (schema `$id`) | Architecture |
| PV intake request/response | In/Out | JSON file/CLI | `pv_response` v1 | Architecture |
| Supply options request/response | In/Out | JSON file/CLI | `supply_response` v1 | Architecture |
| Evidence item | Embedded | JSON object | `evidence_item` v1 | Domain |
| AuthZ check result | Embedded | Object in response | Part of each schema | Security |
| Audit event | Out | Object + export | Audit subset | Evaluation |
| LIMS/MES/QMS/safety/IRT read adapters | In | Fixture snapshots | Evidence item mapping | Build |
| Inference adapter | Internal | Structured suggestion | Non-authoritative annotation | Architecture |

No write interfaces to brownfield systems of record are published.

## 2. Versioned input contracts

Common input fields (all workflows):

| Field | Type | Rule |
|---|---|---|
| `request_id` | string | Non-empty; correlates audit |
| `idempotency_key` | string | Required by Team 3 runtime; unique per intent |
| `workflow` | enum | `batch_evidence` \| `pv_intake` \| `supply_options` |
| `as_of` | string | Instant or dated as-of for applicability |
| `authorization.user` | string | Current user identity |
| `authorization.purpose` | string | Purpose limitation |
| `authorization` context | object | Re-checked at execution; stale → deny |

Workflow-specific inputs:

| Workflow | Required inputs |
|---|---|
| batch_evidence | `batch_id`; purpose; authorized user |
| pv_intake | Source package reference; receipt events; product context |
| supply_options | Shortage/cold-chain `event_id`; inventory snapshot ref; quality status ref; demand/constraints |

## 3. Versioned output contracts

Aligned to E-421..E-425. Shared required outputs: `request_id`, `workflow`, `as_of`, `authorization`, `evidence`, `contradictions`, `gaps`, `abstentions`, `human_review`, `execution_status` (const `not_executed`), `audit`.

| Workflow | Additional required outputs | Explicitly prohibited |
|---|---|---|
| batch_evidence | `batch_id`, `readiness_state`, `applicable_documents` | Any disposition/execution property (e.g. `batch_disposition`, release/reject/reprocess) |
| pv_intake | `case_ids`, `source_facts`, `duplicate_candidates`, `clock_evidence`, `terminology`, `listedness_context`, `required_reviews` | Final seriousness, causality, expectedness, reportability, signal confirmation (e.g. `final_reportability`, `causality_assessment`) |
| supply_options | `event_id`, `options` (each `status: draft`), `constraints`, `approvals_required`, `quality_holds`, `no_side_effects: true` | `no_side_effects: false`; reservation/allocation/shipment/quality-status/recall properties |

`additionalProperties: false` on root response objects enforces fail-closed rejection of unknown/prohibited fields.

## 4. Units and terminology

| Rule | Behaviour | Inject / basis |
|---|---|---|
| Unit present with quantity | Preserve verbatim unit and value | Evidence integrity rules |
| Conversion requested | Only via approved mapping with provenance | INJ-024; D-010 |
| Unapproved mapping | Abstain; record contradiction/gap | Hard gate |
| Terminology (PV) | Preserve source term; attach candidate coding with provenance; human confirms | Case §4 PV |
| Silent normalize | Forbidden | Scoring hard gates |

## 5. Time and identity semantics

| Concern | Rule |
|---|---|
| `as_of` | Applicability filter for documents and snapshots; do not invent future facts |
| `effective_at` | May be null if source lacks it; null forces caution/abstain on time-sensitive claims |
| `retrieved_at` | Wall-clock of retrieval; recorded on every evidence item |
| Identity | Batch, case, material and site identifiers preserved as sourced; collisions surfaced as contradictions (INJ-005/045) |
| Clock evidence (PV) | Receipt/aware/report timestamps listed separately; no silent timezone coercion without provenance |

## 6. Error/idempotency/replay

| Topic | Contract rule |
|---|---|
| Idempotency key | Client supplies `idempotency_key`; server stores response hash for key+workflow+as_of+user |
| Replay identical payload | Return same advisory result; emit audit `replay=true`; never create SoR side effects |
| Replay conflicting payload same key | Reject with conflict error; do not overwrite prior result |
| AuthZ deny | Return deny decision; empty actionable recommendations; audit reason |
| Schema invalid / prohibited field | Fail closed; do not partially apply |
| Budget/stop | Return deterministic partial with abstentions; `execution_status` remains `not_executed` |
| Event semantics | Audit/advisory events only; no command events to inventory or quality status |

## 7. Compatibility and contract tests

| Check | Expected | Location |
|---|---|---|
| positive_batch / pv / supply | Validate clean | `evaluation/contract_samples/` or `submission/tests/fixtures/` |
| negative_batch_prohibited | Fail (`batch_disposition`) | Same |
| negative_pv_prohibited | Fail (`final_reportability`) | Same |
| negative_pv_causality | Fail (`causality_assessment`) | `submission/tests/fixtures/` |
| negative_supply_side_effect | Fail (`no_side_effects: false` and/or `reservation_id`) | Same |
| Runner | Stdlib unittest | `submission/scripts/test.py` / `test.ps1` |
| Helper | Schema validate + prohibited field reject | `submission/src/contracts.py` |

Team 3 extensions must bump a documented version and add compatibility tests; hard-gate prohibitions are never relaxed.

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-421 | Assumption | Package schemas remain minimum executable contracts through defence | Test alignment | Architecture | Package schema change | Accepted |
| R-422 | Decision | `idempotency_key` enforced in runtime even if not in minimum response schema | Implementation must accept and audit key on input | Build | Phase 5 API | Accepted |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Align with WORKFLOW_CONTRACTS | §§2–3 | Contract tests | E-421..E-426 | Tests green |
| Fail-closed prohibited fields | `additionalProperties: false` | Negative fixtures | `submission/tests/` | Tests green |
| Idempotency semantics | §6 | Later runtime tests | ADR-007 | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Build lead | Reviewer | Require local fixtures fallback for offline tests | Fixtures under `submission/tests/fixtures/` | 2026-08-10 |
| Domain/evidence lead | Reviewer | Spell out unit abstention vs silent convert | §4 table | 2026-08-10 |
| Evaluation/reliability lead | Reviewer | Tie acceptance to unittest runner | §7 | 2026-08-10 |
