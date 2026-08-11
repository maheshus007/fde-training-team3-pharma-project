# ADR-AA-017 — Taipy as HITL workbench

- **Status:** accepted (product UI)  
- **Evidence basis:** stakeholder stack preference 2026-08-11; INJ-071 forced evidence viewing  
- **Context:** Previous C4 named generic `submission/app` (static). Product needs an interactive agentic workbench.  
- **Decision:** HITL UI is a **Taipy** app under `submission/app` (or `submission/src/ui`) that binds to the same workflow contracts as CLI. Reviewers must see conflicts/gaps before acknowledgement. No one-click release/allocate.  
- **Alternatives:** Static HTML; Streamlit; React. Rejected in favour of Taipy per product choice.  
- **Drivers:** Python-native UI; faster FDE loop with engines in-process or via local API.  
- **Consequences:** Taipy dependency for UI demo; assessment may still export JSON packs without launching Taipy if documented.  
- **Guardrails:** UI must not bypass policy_guard/contracts; no disposition buttons; accessibility minimum (keyboard) remains.  
- **Validation:** AC-F1 (cannot ack readiness without viewing conflicts); offline/mock data path through Taipy.  
- **Revisit:** Taipy cannot run offline against mocks; then keep CLI as assessment UI.
