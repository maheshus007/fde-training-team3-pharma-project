# Architecture Review / Defense — Prompt 07 (re-validated)

| Field | Entry |
|---|---|
| Date | 2026-08-10 |
| Review status | **conditional** |
| Go-forward | May proceed to Prompt 08 **with conditions below** |

## Defensibility checks

| Check | Result | Notes |
|---|---|---|
| C4 matches DDD bounded contexts and FR-A..F | **PASS** (after DDD v2 + C4 mapping) | Research/Clinical present as adjacency; ACLs in DDD |
| Material trade-offs have ADRs | **PASS** | ADR-AA-* scheme; no collision with scored ADR-010 |
| Trust, authority, privacy, degraded-mode, prohibited writes visible | **PASS** | |
| Gen AI / HITL / rules boundaries on map | **PASS** | GEN_AI_BOUNDARIES §§8–16 |
| PRD out-of-scope not smuggled | **PASS** | KG runtime provisional, not mandatory Answer |
| Offline mode + kill switch | **PASS** | |
| D-205 honesty | **PASS** | Product Cosmos Gremlin (ADR-AA-018); D-205 = assessment GraphPort; CQ proofs still required on the port |

## Open issues / conditions

| ID | Condition before POC “complete” |
|---|---|
| O-1 | CQ-1/3/6 tests green before accepting ADR-AA-015 |
| O-2 | Unify `supply_options` in policy_guard/tests (ADR-AA-012) |
| O-3 | Sync AgenticApp → scored artefacts after IDs stable |
| O-4 | Expand scored artefact 08 only when accepting/rejecting KG with evidence |
| O-5 | Do not claim BR-01 % (Unknown) |

## Prior overclaim corrected

Earlier review asserted DDD↔C4 fit while DDD omitted ACLs/Research/Clinical — **invalidated**. Re-review after DDD v2.0 expansion.

## Go-forward

**conditional** → Prompt 08 SRS with **locked product stack**: Azure OpenAI + Taipy + Cosmos Gremlin, plus mandatory `assessment` adapters. Default CI mode = **assessment**.
