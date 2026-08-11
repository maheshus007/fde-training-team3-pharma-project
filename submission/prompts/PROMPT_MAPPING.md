# Team Prompt Mapping — AEGIS-PHARMA V3

Team method prompts live here. Package control prompts stay immutable in `prompts/PROMPT_LIBRARY.md`.

## Artefact rule (non-negotiable)

- **Workshop plan is authoritative for when artefacts are created.** Follow `WORKSHOP_DEPLOYMENT_PLAN.md` stages (Stage 1 → 01–04; Stage 2 → 05–09; etc.). Do not create later-stage artefacts early.
- Create scored artefacts **only** by copying `templates/NN_*.md` → `submission/artefacts/NN_*.md` and filling them.
- Implementation goes in the scaffold dirs the package already defines: `submission/src`, `app`, `tests`, `evaluation`, `evidence`, `runbooks`, `scripts`.
- Use thin DMAIC notes inside prompts only to fill artefact `02_DMAIC_WORKBOOK.md` when that artefact is in-stage — do not create separate `dmaic_lens.md` files.
- Team prompts may *prepare content* for a later artefact, but scored files are created only in the workshop stage that owns them.

### Exception — AgenticApp SDD working tree

- `submission/AgenticApp/` is the **Spec-Driven Development working tree** for the agentic end-to-end app (prompt runs 01–13, ontology/KG design, feature specs, C4, ADRs, SRS).
- Prompt *runs* write deep outputs there first. After each step gate, promote/merge into `submission/artefacts/NN_*.md` (scored SoT for `--final` / defence) via `AgenticApp/_sync/`.
- Do **not** treat AgenticApp alone as a substitute for the 30 scored artefacts.
- Do not place AgenticApp outside `submission/`.

## How to use

1. Run the team prompt for the phase.
2. Apply the listed package control prompt(s) from `prompts/PROMPT_LIBRARY.md`.
3. Write results into the mapped `submission/artefacts/` file(s) (and scaffold dirs where noted).
4. Respect each team prompt’s entry/exit criteria and GxP fail-closed boundaries.

## Missing threat prompt → use repo approach

There is **no** team `threat` prompt file. For threat/abuse work use the package approach only:

1. Package control prompt **#4** in `prompts/PROMPT_LIBRARY.md` (“Threat-model a design”).
2. Template → artefact: `templates/16_THREAT_ABUSE_MODEL.md` → `submission/artefacts/16_THREAT_ABUSE_MODEL.md`.
3. Optional reviewer: `.cursor/agents/security-reviewer.md`.
4. Also cover related templates when assuring: `17_PRIVACY_ETHICS`, `18_RESPONSIBLE_AI_HUMAN_FACTORS` (same package #4 / #5 discipline).

## Sequencing note (DMAIC)

Workshop Stage 1 wants DMAIC early. Team Prompt 09 is the full Lean/DMAIC consolidation after design.

- Start filling `submission/artefacts/02_DMAIC_WORKBOOK.md` during Prompts 01–08 (Define/Measure content).
- Complete artefact 02 with Prompt 09 before coding tasks (Prompt 10).

## Master mapping

| Team prompt | Package control | Cursor command | Write into (expected artefacts / dirs only) |
|---|---|---|---|
| `01_discovery.md` | #1 Qualify; #2 Map evidence | `00_qualify_problem`; `01_map_evidence` | Stage 1 files only: evidence registers in **01**, **03**; start **02**. (SoT notes for **06** wait until Stage 2) |
| `02_scqa_minto.md` | #1 Qualify | `00_qualify_problem` | **01_BUSINESS_CASE** (SCQA narrative; pitch deferred to Stage 8 / artefact **30**) |
| `03_prd_vision.md` | #1 Qualify | `00_qualify_problem` | **04_PRODUCT_SERVICE_BLUEPRINT**; complete **01**, **03**; continue **02** |
| `04_ddd.md` | #2 Map evidence | `01_map_evidence` | Stage 2: **05**, **07**, **08**; also create/fill **06** and **09** per workshop Stage 2 |
| `05_feature_specs.md` | #3 Derive requirements and tests | `02_build_tests_first` | **09_REQUIREMENTS_TRACEABILITY** |
| `06_c4.md` | #3 | — | **10_C4_ARCHITECTURE**; structure parts of **12_INTEGRATION_CONTRACTS** |
| `07_adrs.md` | #3; #5 Review | — | **11_ADR_REGISTER** (≥10 ADRs for scoring) |
| `08_technical_design.md` | #3 | `02_build_tests_first` | **12_INTEGRATION_CONTRACTS**; participant contracts under `submission/evaluation/` for PUB-09–15 |
| `09_lean_dmaic.md` | #1 | — | **02_DMAIC_WORKBOOK**; feed **22**, **23**, **24** |
| `10_implementation_tasks.md` | #3 | `02_build_tests_first` | Plan only inside **09** / **28** as needed; executable work goes to `submission/tests` + later `src` — no extra task-tree files |
| `11_product_and_build.md` | #5 Review | — | `submission/src`, `submission/app`, `submission/tests` |
| `12_assurance.md` | #4 (repo approach); #5; #6 | — | **13–15**, **16** (via package #4), **17–21**, **22–25**, **28**; `submission/evaluation`, `submission/evidence` |
| `13_solution_proposal.md` | #6 Prepare the defence | — | **26_TARGET_OPERATING_MODEL**; **27_VENDOR_EXIT_RETIREMENT**; **28_PRODUCTION_READINESS**; **29_NINETY_DAY_ROADMAP_HANDOVER**; **30_ELEVATOR_PITCH** |

## Package control prompts ↔ team prompts

| # | Title | Apply with |
|---|---|---|
| 1 | Qualify the problem | 01, 02, 03, 09 |
| 2 | Map evidence authority | 01, 04 |
| 3 | Derive requirements and tests | 05, 08, 10 |
| 4 | Threat-model a design | **Repo approach only** → artefact **16** (see above) |
| 5 | Review a candidate output | 07, 11, 12 |
| 6 | Prepare the defence | 13 + `requirements/FINAL_DEFENCE.md` |

## Mandatory workflows

| Workflow | Contract | Prompts | Must prove |
|---|---|---|---|
| Batch evidence | `evaluation/contracts/batch_response.schema.json` | 04–08, 10–12 | No disposition; `execution_status: not_executed` |
| PV intake | `evaluation/contracts/pv_response.schema.json` | 04–08, 10–12 | No final PV decisions |
| Supply options | `evaluation/contracts/supply_response.schema.json` | 04–08, 10–12 | `no_side_effects: true`; options `draft` only |

## Artefact ownership (30 templates → submission/artefacts)

| Artefact file | Filled by |
|---|---|
| `01_BUSINESS_CASE.md` | 02 + 03 |
| `02_DMAIC_WORKBOOK.md` | 01–08 (start) + 09 (complete) |
| `03_STAKEHOLDER_DECISION_RIGHTS.md` | 01 + 03 |
| `04_PRODUCT_SERVICE_BLUEPRINT.md` | 03 |
| `05_DDD_CONTEXT_MAP.md` | 04 |
| `06_DATA_GOVERNANCE_INTEGRITY.md` | Stage 2 (Prompt 04 + later 08); not Stage 1 |
| `07_ONTOLOGY_SEMANTIC_LAYER.md` | 04 |
| `08_KNOWLEDGE_GRAPH_DECISION.md` | 04 |
| `09_REQUIREMENTS_TRACEABILITY.md` | 05 + 08 |
| `10_C4_ARCHITECTURE.md` | 06 |
| `11_ADR_REGISTER.md` | 07 |
| `12_INTEGRATION_CONTRACTS.md` | 06 + 08 |
| `13_GXP_LIFECYCLE_VALIDATION.md` | 12 |
| `14_COMPUTER_SOFTWARE_ASSURANCE.md` | 12 |
| `15_QUALITY_RISK_MANAGEMENT.md` | 09 + 12 |
| `16_THREAT_ABUSE_MODEL.md` | Package #4 (repo approach) |
| `17_PRIVACY_ETHICS.md` | 12 |
| `18_RESPONSIBLE_AI_HUMAN_FACTORS.md` | 04 + 12 |
| `19_EU_AI_ACT_APPLICABILITY.md` | 12 |
| `20_ISO42001_GOVERNANCE.md` | 12 |
| `21_ASSURANCE_CASE.md` | 12 |
| `22_EVALUATION_SCORECARD.md` | 09 + 12 |
| `23_TOKEN_FINOPS.md` | 09 + 12 |
| `24_RELIABILITY_OBSERVABILITY.md` | 06 + 12 |
| `25_INCIDENT_RECOVERY.md` | 12 |
| `26_TARGET_OPERATING_MODEL.md` | 13 |
| `27_VENDOR_EXIT_RETIREMENT.md` | 13 |
| `28_PRODUCTION_READINESS.md` | 12 + 13 |
| `29_NINETY_DAY_ROADMAP_HANDOVER.md` | 13 |
| `30_ELEVATOR_PITCH.md` | 13 only (Stage 8 Defence) |
