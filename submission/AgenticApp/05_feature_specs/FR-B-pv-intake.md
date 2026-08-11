# FR-B — PV Intake Support

| Field | Entry |
|---|---|
| Actors | PV assessor; system |
| Context | Safety |
| Matching/confidence | Duplicate similarity uses fixture `duplicate_candidates` scores; **no** irreversible merge below/above any threshold — candidates only. Threshold numbers as in CSV; Unknown if absent → show raw score only. |

## Preconditions

- Purpose `pv_intake`; authorized role  
- Source package / case ids / as-of  
- Fresh entitlement  

## Happy path

1. Ingest case facts with verbatim pointers.  
2. Propose duplicate candidates for PV-1001 / PV-1009 / PV-1014 cluster (no merge).  
3. Surface receipt clocks without collapsing awareness dates.  
4. Present listedness by IB/CCDS/local label.  
5. Retain MedDRA version per coding (27.1 vs 28.0).  
6. Segment sensitive content for elevated roles.  
7. Abstain on unauthenticated social-media cases for actionable PV.  
8. Emit required_reviews; execution_status not_executed.  

## Exceptions

- Stale auth → deny  
- Role lacks sensitive segment → omit/deny segment  
- Inference off → rules/fixtures still propose candidates from CSV  

## Business rules

- BR-B1: No final seriousness/causality/expectedness/reportability/signal fields.  
- BR-B2: No auto-merge of cases.  
- BR-B3: Sensitive segments least-privilege (INJ-041).  
- BR-B4: Social authenticity failure blocks actionable use (INJ-042).  

## Acceptance criteria

- AC-B1: Schema-valid pv response.  
- AC-B2: Duplicate candidates include PV-1001, PV-1009, PV-1014 as applicable; merge absent.  
- AC-B3: Conflicting clocks all visible (INJ-038).  
- AC-B4: Listedness sources not collapsed (INJ-040).  
- AC-B5: final_reportability field rejected.  
- AC-B6: Manual/AI-disabled path available.  
- AC-B7: MedDRA versions visible on related codings (INJ-039).  
- AC-B8: Unauthorized role denied sensitive segment (INJ-041).  
- AC-B9: Unauthenticated social case abstained for action (INJ-042).  

## Ambiguities

- Exact “actionable” definition for social cases beyond authenticity flag — treat authenticity failure as abstain.  
- Signal disproportionality metrics (INJ-044) — out of MVP unless added to PRD.

## Out of scope

Final PV decisions; signal confirmation.
