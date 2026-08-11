# Minto Pyramid — Prompt 02 (revised)

## Governing answer

Build a bounded **advisory evidence-reconciliation capability** for Workflows A/B/C with governed semantics, citeable multi-hop evidence, HITL and AI-disabled continuity — not an autonomous decision engine. Architecture (KG runtime, agent topology) is decided later under ADR with evidence.

## MECE supporting points

### 1. Problem is reconciliation latency and opacity — not missing human decision makers
- Support: case §2–4; decision_rights AI authority none/draft only.

### 2. Hard gates forbid automating disposition, final PV, allocation, formulation/spec and eligibility
- Support: `ai_use_boundaries.csv`; INJ-006; scoring hard gates; D-002.

### 3. Deterministic contracts and policy guards are non-negotiable; inference is optional
- Support: D-004; evaluation contracts; `policy_guard.py`; continuity INJ-082.

### 4. Semantic/domain rules are required to stop silent meaning collapse (units, MedDRA, IDMP, clocks)
- Support: INJ-024, 038, 039, 040, 045; ontology competency questions.

### 5. Multi-hop citeable evidence is required for defence-quality packs; **implementation choice** (RER vs offline KG) is an ADR with RER fallback
- Support: CQ-1/3/6; D-205 accepted baseline; provisional ADR-AA-015 if KG runtime pursued.

### 6. Any agentic orchestration adds value only with budgets, signed tools, authZ, checkpoints and HITL
- Support: case §5; AGENT_BUDGET; ZERO_TRUST_AI_TOOLS; INJ-066/067/080/071.

### 7. No-AI / rules path remains a first-class competitor and continuity mode
- Support: INJ-003; D-003; continuity_requirements.csv.
