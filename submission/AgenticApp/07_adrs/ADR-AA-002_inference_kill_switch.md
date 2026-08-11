# ADR-002 — Replaceable inference behind kill switch

- **Status:** accepted  
- **Decision:** Narrow adapter (structured in/out); product implementation is Azure OpenAI (ADR-AA-016); kill switch disables adapter only.  
- **Alternatives:** Embedded model calls in engines; no inference ever.  
- **Guardrails:** Model hash mismatch → fallback (INJ-070).  
- **Validation:** Kill-switch drill leaves rules/KG/HITL up.
