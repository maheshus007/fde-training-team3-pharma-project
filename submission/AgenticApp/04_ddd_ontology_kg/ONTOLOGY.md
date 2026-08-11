# Ontology — AEGIS AgenticApp (deepened)

| Field | Entry |
|---|---|
| Status | stable for POC concepts |
| Seed | `artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md` |

## Core concepts

Organisation, MedicinalProduct, Substance, Batch, MaterialLot, LabResult, QualityEvent, IcsrCase, AdverseEventCoding, ListednessAssertion, Shipment, TemperatureObservation, MarketAuthorisation, EvidenceFact, Mapping, AgentRun, ToolManifest, EntitlementCheck, ProvenanceStamp, PurposeCode.

## Key relations

`consumed` / `missing_branch` / `issued`; `coded_as` (MedDRA versioned); `listed_in` / `not_listed_in`; `aliased_as`; `constrained_by`; `observed_under_time_context`; `evidenced_by`; `mapped_to` with `mapping_status` ∈ {approved, ambiguous, rejected, unknown}; `duplicate_candidate_of`.

## Identifiers and aliases

| Scheme | Example | Rule |
|---|---|---|
| NTG product | NCB-204 | Prefer when mapping unambiguous |
| ERP product | NCB204-DE | Retain; do not auto-equate |
| Alias | NCB204, brand_alias_B | Search only |
| Batch | NCB204-B24071 | Shared kernel |
| Material lot | SUA-88 | Independent |
| Case | PV-1001, PV-1009, PV-1014 | Safety namespace; INJ-037 triad |
| Org prefix | BIOX\|, NTG\|, CMO-IE\| | Required (INJ-005) |

## Constraints

1. EvidenceFact requires full provenance.  
2. Unit conversion requires approved Mapping.  
3. MedicinalProduct merge forbidden when mapping_status ≠ approved.  
4. IcsrCase merge forbidden by system.  
5. No disposition/allocate/ship/recall/signal_confirmed relations.  
6. MedDRA version retained on every coding (27.1 vs 28.0 coexistence).  

## Temporal / jurisdictional (from seed §4)

Effective date, knowledge vs event time, timezone/`timezone_unknown`, precision, jurisdiction, supersession — never project facts across applicability without record.

## Agent tool intents

`ResolveConcept`, `GetProvenance`, `FindConflicts`, `TraverseEvidencePath`, `AssessReadiness`, `ProposeDuplicateCandidates`, `EnumerateDraftOptions`, `RequestHumanReview`.
