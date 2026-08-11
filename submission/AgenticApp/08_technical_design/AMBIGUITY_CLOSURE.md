# SRS — Spec ambiguity closure (Prompt 08 §H)

| Source | Item | Resolution | Revisit |
|---|---|---|---|
| FR-A | Readiness when contradictions exist | **Assumed:** `conflicted_evidence` | If examiner wants ready+listed conflicts |
| FR-A | CAPA taxonomy similarity | **Open-blocked:** no auto-link; out of MVP | — |
| FR-B | Duplicate threshold | **Assumed:** emit all `duplicate_candidates.csv` rows for requested cases; no extra numeric gate | If CSV empty |
| FR-B | INJ-044 signal metrics | **Open-blocked** (PRD out of scope) | — |
| FR-C | Option ranking weights | **Assumed:** stable sort by `option_id` unless inference hint present; hints never execute | Artefact 23 |
| FR-D | Budgets | **Assumed:** 20 steps, 30 tools, 3 LLM calls, 2048 tokens, T=0 | Artefact 23 |
| FR-E | KG default | **Resolved:** assessment GraphPort default; Cosmos only `cloud` | — |
| FR-F | WCAG level | **Assumed:** keyboard access to 4 pages; not WCAG AA claim | INJ-073 later |
| PRD | Azure deployment name | **Open** until env provided; assessment does not need it | cloud demo |
| PRD | Cosmos db/graph names | **Assumed env:** `COSMOS_GREMLIN_DATABASE=aegis`, `COSMOS_GREMLIN_GRAPH=evidence` | cloud demo |
| Auth | Azure AD | **Resolved:** out of POC; fixture entitlements | — |
| HTTP | Required? | **Assumed:** Python `service.py` sufficient; HTTP optional | — |
| Product repo layout | Enterprise SDLC image vs package dirs | **Resolved:** product in `submission/aegis-sdd/`; scoring shims stay under `submission/src|app|tests` | do not git-init unless asked |
| Cloud graph down | Fail vs fallback | **Assumed:** `AEGIS_GRAPH_FALLBACK=true` → memory port | Set false for 504 |
| Budget vs HTTP 429 | Conflict in first SRS draft | **Resolved:** submit returns valid pack + abstention `budget_exhausted` | — |
| Request `runtime_mode` | Could override assessment | **Resolved:** withdrawn; env only | — |
| `as_of` Z vs offset | Fixtures use `Z` | **Resolved:** both allowed | — |
| human_review.acknowledged on response | Would be extra vs samples | **Resolved:** ack in audit store only | — |
| IDMP matching order | FR-E checklist | **Resolved:** exact → alias → stop (no fuzzy) | — |
| PUB-09–15 files | Prompt 08 vs later stage | **Open-blocked** until Prompt 11/12 | scoring evaluation |
| sha256 of what | Unspecified | **Resolved:** canonical JSON `facts` | — |
| Azure retries | Unspecified | **Resolved:** 0 + optional 1 on 408/429 | — |
