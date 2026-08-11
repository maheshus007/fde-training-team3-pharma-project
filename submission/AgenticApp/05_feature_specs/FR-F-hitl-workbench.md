# FR-F — HITL Workbench

| Field | Entry |
|---|---|
| Matching/confidence | N/A |

## Preconditions

- Authenticated reviewer; workflow pack available  

## Happy path

1. Present evidence items before readiness banner.  
2. Require acknowledgement of contradictions/gaps.  
3. Support AI-disabled view of same pack.  
4. Export audit trail.  

## Exceptions

- Conflicts exist but not viewed → block human-ack  
- Kill switch on → show rules-only banner  

## Business rules

- BR-F1: No one-click “approve release”.  
- BR-F2: Forced evidence viewing (INJ-071).  

## Acceptance criteria

- AC-F1: Readiness cannot be human-acked without viewing conflict list when conflicts exist.  
- AC-F2: Workbench is **Taipy** under `submission/app`; assessment mode binds mock/RER data (no Azure keys).  
- AC-F3: Basic keyboard-accessible navigation (INJ-073 minimum).  

## Ambiguities

- Full WCAG level target — Unknown; minimum keyboard nav for POC.
