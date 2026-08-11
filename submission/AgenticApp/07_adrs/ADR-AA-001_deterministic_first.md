# ADR-001 — Deterministic-first execution path

- **Status:** accepted  
- **Evidence basis:** fact (continuity CSV; D-004)  
- **Context:** Need offline reliability and no-AI competitor parity.  
- **Decision:** Default path is rules/fixtures reconciliation; inference optional.  
- **Alternatives:** LLM-first agent; rules-only forever.  
- **Consequences:** Higher auditability; less “AI showcase” optics.  
- **Guardrails:** Inference cannot be sole path for ACs.  
- **Validation:** AI-disabled tests pass core ACs.  
- **Revisit:** If rules alone fail measured evaluation with hard gates intact.
