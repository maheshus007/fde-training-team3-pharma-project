# AgenticApp pipeline assumptions (validated)

| ID | Statement | Status |
|---|---|---|
| AA-001 | AgenticApp working tree allowed; scored SoT = `submission/artefacts/` | Accepted |
| AA-002 | Target capability is advisory A/B/C with governed semantics + citeable multi-hop evidence + HITL | Accepted |
| AA-003 | Assessment GraphPort (in-memory/RER) can prove CQ-1/3/6 without Cosmos | Open until tests exist |
| AA-004 | Phase 0–4 artefacts are evidence seeds; deepen rather than discard | Accepted |
| AA-005 | BR-01 measured baseline remains Unknown until evaluation | Accepted |
| AA-006 | Hard gates from `ai_use_boundaries.csv` + INJ-006 remain binding | Accepted |
| AA-007 | `generate_phase2_to4.py` must not be re-run unguarded | Accepted |
| AA-008 | Framing mode `decision-ready` for scope; architecture options provisional | Accepted |
| AA-009 | ADR IDs use `ADR-AA-*` to avoid colliding with scored ADR-001..012 | Accepted |
| AA-010 | D-205 describes assessment fallback; product graph is Cosmos Gremlin (ADR-AA-018) | Accepted |
| AA-011 | Product LLM is Azure OpenAI; assessment uses InferencePort stub (ADR-AA-016) | Accepted |
| AA-012 | Product UI is Taipy (ADR-AA-017); UI must not bypass policy_guard | Accepted |
| AA-013 | `AEGIS_RUNTIME_MODE` default is `assessment` so examiners need no Azure keys | Accepted |
