# C4 Level 2 — Containers

| Field | Entry |
|---|---|
| Artifact status | **stable** for product stack 2026-08-11 (Azure OpenAI + Taipy + Cosmos Gremlin); assessment adapters mandatory |

| Container | Responsibility | Tech stance | FR mapping | DDD context |
|---|---|---|---|---|
| Advisory API / CLI | Envelope, budgets, routing | Python `submission/` | FR-D | Platform |
| Deterministic reconciliation engine | Workflows A/B/C rules | Fixtures + rules | FR-A/B/C | Mfg/Lab/Quality/Safety/Supply |
| Ontology / semantic service | Concept resolve, unit/MedDRA/IDMP/time policy | Versioned rules | FR-E | Platform + Regulatory/Lab/PV |
| Evidence graph (`GraphPort`) | Multi-hop citation | **Cloud:** Cosmos Gremlin. **Assessment:** in-memory/RER | FR-E | Platform |
| Agent runtime | Tool loop, checkpoints | Python orchestrator; Azure OpenAI in `cloud` | FR-D | Platform |
| Inference adapter | Structured suggestions | **Azure OpenAI** + kill switch; stub in assessment | FR-D | Platform |
| Policy guard + contract validator | Fail-closed | Existing modules | All | Platform |
| HITL workbench | Forced evidence view | **Taipy** | FR-F | All reviewers |
| Audit / evidence export | Append-only | `submission/evidence` | All | Platform |

## Boundaries

- Trust: untrusted retrieval cannot drive tools  
- Privacy: purpose + role segment filters  
- Authority: deny stale entitlements  
- Connectivity: offline fixtures primary  

## Degraded / offline

Inference kill switch → rules + GraphPort (assessment or Cosmos read) + Taipy remain; Azure OpenAI off.

## Prohibited write paths

No container emits disposition, final PV, reservation/allocation/shipment/recall, quality-status change, or eligibility decisions to SoR.
