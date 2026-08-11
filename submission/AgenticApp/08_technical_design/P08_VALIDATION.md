# Prompt 08 validation (blindspot audit)

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Verdict | **Gaps from first SRS draft closed.** Remaining items are labeled assumed/open-blocked, not unmarked. |

## Prompt 08 Produce coverage

| Section | File | Status |
|---|---|---|
| A APIs | SRS_API_CONTRACTS + INTERNAL_OBJECT_SHAPES | Complete after patch |
| B Data model | DATA_MODEL_AND_KG_SCHEMA | Complete (LIMS v1/v2, sha256, forbidden edges) |
| C State | STATE_TRANSITIONS | Complete |
| D NFRs | NFRS (01–20) | Complete; numeric |
| E Errors/security | ERROR_AND_SECURITY | Complete; budget/503 clarified |
| F Modules | MODULE_LAYERING | Complete |
| G Trace matrix | TRACEABILITY_MATRIX | Complete |
| H Ambiguity | AMBIGUITY_CLOSURE | Complete |
| H2 Gap audit | artefact **09** + TRACEABILITY_MATRIX | Complete (was missing from 09) |
| I Deploy | DEPLOYMENT_NOTES | Complete |
| DMAIC thin | artefact 02 | Already appended |

## Blindspots found in first draft → fix

| Blindspot | Severity | Fix |
|---|---|---|
| Nested contradiction/gap/abstention/PV/supply shapes unspecified | Critical | INTERNAL_OBJECT_SHAPES |
| CQ-2..5,7..9 params missing | Critical | §6 CQ table |
| Tool allowlist / manifest (AC-D1) missing | Critical | §7 |
| Checkpoint resume (AC-D3) missing | Major | resume_checkpoint_id + §8 |
| AC-A6/A7/B8/B9/C5 not mapped to fields | Major | kinds/codes/channels |
| H2 not in artefact 09 | Major | appended |
| Budget AEGIS-429 vs artefact 12 partial pack | Critical contradiction | submit = 200 + abstention |
| Request `runtime_mode` could override assessment | Major | withdrawn; env only |
| `as_of` forbade `Z` used by fixtures | Major | Z allowed |
| human_review.acknowledged would break sample shape | Major | ack in audit store only |
| sha256 input unspecified | Major | canonical facts JSON |
| Azure retries unspecified | Minor | 0 + one 408/429 |
| Model hash env missing | Major (INJ-070) | AZURE_OPENAI_MODEL_HASH |
| Graph unbounded paths | Minor | max 50 |
| LIMS v1/v2 ACL | Major | DATA_MODEL §6 |
| PUB-09–15 silent omit | Minor | explicit defer |
| authorization.role missing (INJ-041) | Major | request.role |
| ingest_graph not a service op | Minor | added |

## Still open (marked, not unmarked)

- Azure deployment name (cloud demo only)
- CAPA auto-link (out of MVP)
- INJ-044 (out of PRD)
- WCAG AA (keyboard min only)
- PUB-09–15 files (Prompt 11/12)
- `AEGIS_GRAPH_FALLBACK` product may later forbid

## Exit criteria

- [x] APIs/data/state/NFRs/errors for governed slice  
- [x] Traceability covers FR-A..F  
- [x] H2 in artefact 09; no unmarked orphans  
- [x] Matching thresholds assumed or ordered  
- [x] Open items labeled  
- [x] Numeric NFRs  
- [x] C4/ADR guardrails  
- [x] Artefact 12 addendum  
- [x] DMAIC thin notes  
- [x] No feature coding in this prompt  
