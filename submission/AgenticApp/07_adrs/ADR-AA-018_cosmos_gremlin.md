# ADR-AA-018 — Azure Cosmos DB Gremlin as product graph

- **Status:** accepted (product graph); assessment uses in-memory/RER port  
- **Evidence basis:** stakeholder preference 2026-08-11; CQ-1/3/6 multi-hop citation; D-205 remains the *assessment* default until dual-path proven  
- **Context:** D-205 rejected a graph *DB* for POC to avoid vendor lock. Product now explicitly wants Cosmos Gremlin. Package still requires no-key assessment.  
- **Decision:** Product `GraphPort` implementation is **Azure Cosmos DB (Gremlin API)**. Vertices/edges follow ontology; every edge carries provenance properties; agent **cannot** add forbidden write edge labels (`RESERVED_FOR`, `ALLOCATED_TO`, `SHIPPED_AS`, `DISPOSITION_SET`, `SIGNAL_CONFIRMED`). Assessment/default CI uses the same port with an in-memory Gremlin-like or RER traversal. Rebuild/ingest from challenge CSVs; Cosmos is not the system of record.  
- **Alternatives:** (A) RER-only (D-205) — assessment default. (B) Neo4j — rejected. (C) SQLite edge tables — superseded as *product* graph. (D) Cosmos Gremlin — **chosen for product**.  
- **Drivers:** Citeable multi-hop; Azure alignment with OpenAI; Gremlin portable queries vs proprietary SQL-only.  
- **Consequences:** Account, RU cost, residency, secrets, vendor concentration (INJ-078/083); dual-path test cost; artefact 08 / D-205 must be updated to “product graph + RER assessment fallback”, not silent delete of D-205.  
- **Guardrails:** No secrets in git; purpose/as-of/trust filters on traversals; ingest-only from fixtures/ACL; fail closed if Cosmos unreachable in `cloud` mode (do not invent edges).  
- **Validation:** CQ-1/3/6 on in-memory port first; optional live Cosmos demo; forbidden-edge tests.  
- **Revisit:** Cosmos unavailable in workshop; RU cost; examiner insists D-205-only — then product demo optional, assessment still RER.
