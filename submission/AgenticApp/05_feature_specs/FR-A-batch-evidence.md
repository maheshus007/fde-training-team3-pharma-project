# FR-A — Batch Evidence Reconciliation

| Field | Entry |
|---|---|
| Actors | QP/QA reviewer; system rules engine |
| Context | Manufacturing + Quality + Laboratory |
| Matching/confidence checklist | **N/A** (no fuzzy product match gate in this feature; identity conflicts use IDMP ambiguity rules in FR-E) |

## Preconditions

- Authorized user; purpose `batch_review_readiness`  
- `batch_id` + as-of time  
- Entitlement fresh at execution  

## Happy path

1. Load batch-related evidence via ACL/fixtures.  
2. Resolve concepts via ontology (batch ≠ material_lot).  
3. Traverse evidence paths for genealogy; surface MISSING_BRANCH vs ISSUED.  
4. Evaluate lab results; abstain if unit mapping unapproved.  
5. Surface OOS vs OOT vs invalid disagreements without collapse.  
6. Flag QP packet gaps (e.g. missing supplier audit commitment).  
7. Emit pack: evidence, contradictions, gaps, abstentions, readiness_state.  
8. Require human review acknowledgement before treating as accepted.

## Exceptions / alternate paths

- Stale auth → AuthorizationDenied  
- Untrusted document as instruction → ignore as policy; flag  
- Inference off → same detections via rules  
- Ambiguous product identity → IdentityConflict; no silent product swap  

## Business rules

- BR-A1: No disposition/release/reject/reprocess/relabel/recall/quality-status-change fields.  
- BR-A2: Preserve both sides of genealogy conflict.  
- BR-A3: Unapproved unit map ⇒ abstain.  
- BR-A4: Every EvidenceFact has provenance.  
- BR-A5: OOS/OOT/invalid statuses retained distinctly.  

## Acceptance criteria

- AC-A1: Response validates against batch schema.  
- AC-A2: For NCB204-B24071/SUA-88, both MES missing_branch and warehouse issued appear.  
- AC-A3: LR-88 yields abstention when mapping unapproved.  
- AC-A4: Payload with batch_disposition rejected.  
- AC-A5: AI-disabled mode still meets AC-A2/A3.  
- AC-A6: OOS vs OOT vs invalid all visible when present (INJ-023).  
- AC-A7: Missing supplier audit commitment surfaced as gap (INJ-028).  

## HITL / AI

AI may summarize conflicts; rules decide abstention; human owns disposition.

## Ambiguities

- Numeric similarity threshold for “related deviation” taxonomy — Unknown; do not auto-link as same CAPA.  
- Exact readiness_state thresholds beyond schema enums — use schema enums only.

## Out of scope

Executing release/recall; writing to MES/LIMS; formulation/spec change.
