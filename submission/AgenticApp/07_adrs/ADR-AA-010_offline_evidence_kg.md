# ADR-AA-015 — Evidence graph runtime (updated 2026-08-11)

> Canonical ID: **ADR-AA-015**. Filename legacy `ADR-AA-010_offline_evidence_kg.md`. Do not confuse with scored ADR-010 (budgets).  
> Product graph implementation: **ADR-AA-018 (Cosmos Gremlin)**.

- **Status:** **accepted as dual-path** — product = Cosmos Gremlin; assessment = in-memory/RER  
- **Evidence basis:** CQ need + 2026-08-11 stack decision; D-205 X-triggers still not fired for *dropping* RER  
- **Context:** Earlier draft proposed SQLite/in-memory only and left KG `proposed`. Product now specifies Cosmos Gremlin. Scoring still needs a no-key graph port.  
- **Decision:** There **is** an evidence graph in the architecture. **Product** store = Azure Cosmos DB Gremlin API (ADR-AA-018). **Assessment / AI-disabled** store = in-memory property graph or RER traversals implementing the same `GraphPort`. Logical ontology (nodes/edges/provenance/forbidden labels) is identical in both. D-205 is **not deleted**; it describes the assessment fallback, not the product target.  
- **Alternatives:** RER-only product (rejected by stakeholder); SQLite-only product (superseded); Neo4j (rejected).  
- **Guardrails:** Same as ADR-AA-018; CQ proofs required on the **port**, not only on Cosmos.  
- **Validation:** CQ-1/3/6 on assessment port **before** claiming cloud graph success.  
- **Revisit:** If assessment port cannot prove CQs, do not claim KG capability in defence.
