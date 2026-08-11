# Reuse from Phase 0–4 (seed inventory)

Complete before Prompt 01. Cite paths; mark Inherit / Deepen / Supersede / Ignore.

| Asset | Path | Disposition | Notes |
|---|---|---|---|
| Business case / SCQA seed | `submission/artefacts/01_BUSINESS_CASE.md` | Deepen into AgenticApp `02_scqa/` | Strong SCQA-equivalent already |
| DMAIC | `submission/artefacts/02_DMAIC_WORKBOOK.md` | Inherit + thin updates per prompt | Complete with Prompt 09 later |
| Stakeholders | `submission/artefacts/03_STAKEHOLDER_DECISION_RIGHTS.md` | Inherit | |
| Blueprint | `submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md` | Deepen via Prompt 03 | |
| DDD | `submission/artefacts/05_DDD_CONTEXT_MAP.md` | Deepen | High quality; add agent/HITL detail |
| Data governance | `submission/artefacts/06_DATA_GOVERNANCE_INTEGRITY.md` | Inherit | |
| Ontology/semantic | `submission/artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md` | Deepen | CQ-1..7 keep; expand for agent tools |
| KG decision D-205 | `submission/artefacts/08_KNOWLEDGE_GRAPH_DECISION.md` | **Supersede via ADR** | Offline evidence KG + RER fallback |
| Requirements / TEST-* | `submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md` | Deepen | Replace planned TEST IDs with real ACs |
| C4 | `submission/artefacts/10_C4_ARCHITECTURE.md` | Deepen | Add KG + agent containers |
| ADRs | `submission/artefacts/11_ADR_REGISTER.md` | Deepen | Add KG supersession ADRs |
| Integration contracts | `submission/artefacts/12_INTEGRATION_CONTRACTS.md` | Defer to Prompt 08 | |
| Phase 4 assurance 13–21 | `submission/artefacts/13`–`21` | Inherit | Refresh after build |
| Evidence map | `submission/artefacts/EVIDENCE_MAP.md` | Inherit as Discovery input | |
| Assumptions/decisions | `submission/artefacts/ASSUMPTIONS_AND_DECISION_LOG.md` | Append pipeline decisions | |
| Policy guard | `submission/src/policy_guard.py` | Inherit (hard gate) | Fix supply workflow name later |
| Contracts | `submission/src/contracts.py` | Inherit | Canonical `supply_options` |
| Hard-gate tests | `submission/tests/` | Inherit | Extend with feature ACs |
| Generator | `submission/scripts/generate_phase2_to4.py` | **Do not re-run unguarded** | Overwrites deepened docs |
| Challenge explorer | `app/` (repo root) | Ignore for product | Not the AgenticApp UI |
| Package prompts | `prompts/PROMPT_LIBRARY.md` | Apply as controls | Immutable |
| Team prompts | `submission/prompts/*.md` | Execute in order | SoT for Produce sections |

## Framing hypothesis for Discovery

Expected framing mode after Prompt 01: **`decision-ready`** for problem/scope (case pack complete); **`provisional`** only where measured baselines (cycle time %) remain Unknown.
