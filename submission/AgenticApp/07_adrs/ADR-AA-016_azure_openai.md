# ADR-AA-016 — Azure OpenAI as product LLM

- **Status:** accepted (product); assessment uses stub  
- **Evidence basis:** stakeholder stack preference 2026-08-11; still bound by D-004 (inference optional) and INJ-070/082  
- **Context:** Team wants a real agentic app, not stdlib-only inference. Package forbids secret-dependent assessment.  
- **Decision:** Product inference adapter is **Azure OpenAI** (deployment-based chat; **structured JSON** matching workflow schemas). Engines remain deterministic; the model may *suggest* clusters/rankings/narratives, never write SoR or prohibited fields. Kill switch disables this adapter only.  
- **Alternatives:** (A) No LLM (rules only) — rejected as product UX; kept as `ai_disabled` / assessment stub. (B) Other cloud LLMs — rejected; Azure OpenAI chosen. (C) Embed model calls inside engines — rejected (ADR-AA-001/002).  
- **Drivers:** Agentic UX; enterprise identity already Azure-oriented; structured output for fail-closed contracts.  
- **Consequences:** Keys, network, cost, model-hash pinning, denial-of-wallet budgets; must ship stub path.  
- **Guardrails:** `additionalProperties: false` on model JSON; policy_guard on every suggestion; no tools that write disposition/PV finals/allocate; purpose-bound prompts; untrusted docs are data.  
- **Validation:** Cloud demo optional; assessment tests pass with stub; kill-switch test; schema reject of prohibited fields from model.  
- **Revisit:** Azure outage, deployment hash mismatch, cost over budget.
