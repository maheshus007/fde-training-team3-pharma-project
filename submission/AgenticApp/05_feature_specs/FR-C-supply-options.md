# FR-C — Supply Options Planning

| Field | Entry |
|---|---|
| Actors | Supply planner; Quality (holds); system |
| Context | Supply |
| Matching/confidence | N/A for SKU fuzzy match in MVP; channel/ethics constraints are rule flags |

## Preconditions

- Purpose `supply_options` (canonical enum)  
- Shortage/cold-chain event id; inventory + quality + constraint snapshots  
- Fresh entitlement  

## Happy path

1. Load inventory/quality/MA/constraints.  
2. Flag cold-chain logger/pallet/time disputes (SH-901 / LG-31 / P-88 vs P-89).  
3. Enumerate draft options with citations including trial/compassionate/commercial channels.  
4. Attach approvals_required and quality_holds.  
5. Force `no_side_effects: true`; options status `draft`.  

## Exceptions

- Stale auth → deny  
- Association unresolved → abstain on authenticated excursion claims  
- Quarantined stock → not presented as freely allocatable  

## Business rules

- BR-C1: Never create reservation/allocation/shipment/recall ids.  
- BR-C2: Held/quarantined stock constraints visible.  
- BR-C3: Ethics/channel constraints visible (INJ-056).  

## Acceptance criteria

- AC-C1: Schema-valid supply response with no_side_effects true.  
- AC-C2: SH-901 association conflict surfaced (LG-31, P-88 vs P-89).  
- AC-C3: Payload with reservation_id rejected.  
- AC-C4: AI-disabled enumeration still produces draft options from rules.  
- AC-C5: Trial/compassionate/commercial constraint flags present when fixture demands (INJ-056).  

## Ambiguities

- Ranking weights for options — Unknown; rank must be explainable by cited constraints or marked provisional.  
- Recall-scope completeness (INJ-058) — advisory gap listing only; no recall initiation.

## Out of scope

Reserve/allocate/ship/recall execution; quality-status change.
