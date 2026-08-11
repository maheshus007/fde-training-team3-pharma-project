# Semantic Layer — AEGIS AgenticApp (deepened)

## Canonical policies

| Policy | Rule | Evidence |
|---|---|---|
| Units | Compare only under approved interface mapping; else abstain | INJ-024; D-010 |
| MedDRA | Retain version on each coding; flag cross-version grouping | INJ-039; terminology_versions 27.1 vs 28.0 |
| Listedness | Present per IB/CCDS/local label + jurisdiction; no global collapse | INJ-040; IN local label vs CCDS |
| IDMP | Surface ambiguous mappings; stewardship gate | INJ-045; K-015 |
| Time | Preserve precision + timezone; never invent UTC | INJ-018/038/051 |
| Purpose-bind | Request purpose must match entitlement purpose at execution | case §5; INJ-067 authZ freshness (not INJ-060) |
| Consent / secondary use | Training/export on EU trial data blocked without purpose match | **INJ-060** (privacy — separate from entitlement string match) |
| Trust | Untrusted/draft/superseded docs cannot drive actions | INJ-065 |
| Quality status | Keep source strings; do not hide OOS vs OOT vs invalid | INJ-023 |

## Access contracts

- Purposes: `batch_review_readiness`, `pv_intake`, `supply_options`  
- Sensitive PV segments least-privilege (INJ-041)  
- Deny-by-default on stale entitlement cache (INJ-067)  
- Ontology cannot grant disposition powers (`ai_authority`)

## Metrics

ConflictSurfaced; AbstentionCorrect; ProhibitedActionBlocked; PathCitationComplete; MedDRAVersionPreserved; IdmpAmbiguitySurfaced.
