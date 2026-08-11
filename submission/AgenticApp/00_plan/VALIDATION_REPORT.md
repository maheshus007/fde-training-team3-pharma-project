# Validation Report — AgenticApp Prompts 01–07

| Field | Entry |
|---|---|
| Date | 2026-08-10 |
| Scope | Accuracy / gap closure after audit |
| Verdict | **Critical DDD and decision-honesty gaps closed**; residual conditions remain for build |

## Critical findings → resolution

| ID | Finding | Resolution |
|---|---|---|
| C1/C2 | DDD thin vs seed / Prompt 04 | Rewrote `DDD_CONTEXT_MAP.md` v2.0 with evidence register, full UL, Research/Clinical, ACL table, ownership, events, risks, Gen AI index |
| C3 | D-205 silently “accepted” superseded | ADR-AA-015 **proposed**; D-205 remains accepted; RER default; D-KG-001 → Proposed |
| C4 | ADR-010 number collision with scored register | Renamed scheme to **ADR-AA-***; KG = ADR-AA-015 |
| C5 | SCQA Answer locked architecture | Softened to capability-level; KG/agent deferred to ADR |
| C6 | Incomplete never-alone list | Added formulation/spec, eligibility, quality-status, signal confirmation |
| C7 | Architecture review overclaim | Re-reviewed after DDD v2; status still conditional with honest notes |

## Major fixes

- GEN_AI_BOUNDARIES expanded to Prompt 04 §§8–16  
- Ontology/Semantic deepened (MedDRA versions, temporal, INJ-060 vs purpose-bind clarified)  
- CQ-3 includes **PV-1009**; discovery ellipsis fixed  
- FR-A..F: Ambiguities, matching N/A, exceptions, missing ACs (INJ-023/028/039/041/042/056)  
- C4: artifact status + FR/context mapping; KG container provisional  
- PRD out-of-scope expanded  

## Residual blindspots (accepted debt)

| Item | Why residual | Next |
|---|---|---|
| Artefact sync 01/04–11 not fully merged | Working tree first | `_sync` execution |
| DMAIC artefact 02 not fully rewritten | Thin notes in DDD/Discovery only | Prompt 09 |
| ADR-AA stubs 003–009 still shorter than Prompt 07 ideal | Content correct; less defence prose | Optional expand |
| `policy_guard` `supply_planning` string | Code not changed in this validation pass | First Prompt 08/11 task |
| CQ automated tests absent | Expected — build phase | Gate ADR-AA-015 |

## Factual accuracy checklist

| Claim | Status |
|---|---|
| INJ-021 SUA-88 / NCB204-B24071 | OK |
| INJ-024 LR-88 abstain | OK |
| INJ-037 PV-1001/1009/1014 | OK (fixed) |
| INJ-051 SH-901 / LG-31 / P-88/P-89 | OK |
| INJ-045 NCB-204 vs NCB204-DE | OK |
| Purpose-bind ≠ INJ-060 | OK (fixed) |
| D-205 still accepted | OK (fixed) |

## Prompt 04 exit criteria

- [x] Artifact status stated (stable + provisional KG)  
- [x] Ubiquitous language + contexts explicit  
- [x] Rules vs AI vs HITL written  
- [x] RAG/agent map to domain artefacts  
- [x] Domain not organized by CSV filenames  
- [x] Ready for feature specs  
- [ ] Artefact 02 full DMAIC — deferred Prompt 09 (thin notes present)
