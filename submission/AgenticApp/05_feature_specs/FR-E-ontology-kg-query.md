# FR-E — Ontology & Evidence-Path Query

| Field | Entry |
|---|---|
| Matching/confidence | IDMP / alias matching: exact → alias search → **never** auto-approve ambiguous; fuzzy product equate **forbidden** without stewardship |

## Preconditions

- Purpose-bound session; ontology tables loaded  

## Happy path

1. Resolve concepts via ontology.  
2. Answer CQ-1..CQ-7 via RER and/or provisional KG index.  
3. Return edges/facts with provenance.  
4. Abstain when mapping/trust insufficient.  

## Exceptions

- Ambiguous IDMP → conflict object, not merge  
- Untrusted node → not usable as instruction  

## Business rules

- BR-E1: No fabrication of missing genealogy links.  
- BR-E2: Ambiguous IDMP remains ambiguous.  
- BR-E3: Rebuild-from-fixtures deterministic.  
- BR-E4: Default assembly path RER until ADR-AA-015 accepted.  

## Acceptance criteria

- AC-E1: CQ-1 conflict pair for INJ-021.  
- AC-E2: CQ-2 abstains on LR-88.  
- AC-E3: CQ-6 surfaces LG-31 / P-88 vs P-89.  
- AC-E4: Forbidden write edge types cannot be inserted.  
- AC-E5: CQ-3 includes PV-1009 when present in fixtures.  

## Ambiguities

- Whether KG runtime is on by default — **No** until ADR-AA-015 accepted.
