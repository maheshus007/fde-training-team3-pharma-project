# Knowledge Graph Design — Offline Evidence KG

| Field | Entry |
|---|---|
| Status | **accepted dual-path** (2026-08-11) |
| Decision record | ADR-AA-015 + **ADR-AA-018** |
| Relationship to D-205 | D-205 remains assessment/RER fallback; **product** graph is Azure Cosmos DB Gremlin API |
| Prompt | 04 (KG pack) |

## 1. Decision proposal (ADR-AA-015)

**Product:** Azure Cosmos DB (Gremlin API) via `GraphPort`.  
**Assessment / default CI:** in-memory graph or RER implementing the same port (no Cosmos account required).  
**Reject** Neo4j. **Reject** cloud-only with no mock port.

## 2. Why not accept yet

| Gate | State |
|---|---|
| D-205 X-1..X-3 | Not fired |
| CQ automated tests | Not implemented |
| Artefact 08 sync | Pending |
| AA-003 | Remains assumption until validation |

## 3–8. Technical design (unchanged intent)

Node/edge types, provenance schema, query patterns, security filters, and rebuild-from-fixtures grain are as previously specified:

- Forbidden edges: RESERVED_FOR, ALLOCATED_TO, SHIPPED_AS, DISPOSITION_SET, SIGNAL_CONFIRMED  
- Ingest from fixtures only (read-oriented)  
- Filter by purpose/role/as-of/trust_status at query time  

Full edge/node tables retained from prior draft for SRS Prompt 08 — **implementation gated** on ADR-AA-015 acceptance.
