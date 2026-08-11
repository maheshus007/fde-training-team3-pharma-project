# Evidence Acquisition Backlog — Prompt 01

| Priority | Artifact needed | Source | Blocks | Notes |
|---|---|---|---|---|
| P0 | Measured release-packet readiness cycle time | Evaluation fixtures / simulated baseline | BR-01 claim precision | Mark Unknown until Phase 6 |
| P0 | Unify workflow enum `supply_options` | Code + tests | Orchestrator correctness | Existing split is a defect |
| P1 | Fixture packs for INJ-021/024/037/038/040/051 end-to-end | `data/` + PUB-01..08 | Feature ACs | Prefer public fixtures as inputs |
| P1 | Signed tool manifest set for agent tools | `submission/tests/fixtures` pattern | Agent runtime | Extend approved/poisoned samples |
| P1 | Ontology CQ executable proofs | AgenticApp KG design | Ontology/KG acceptance | After Prompt 04 |
| P2 | Accessibility checklist for workbench | INJ-073 | UI defence | Phase 5 app |
| P2 | Token/cost budget numbers | AGENT_BUDGET policy + FinOps artefact | ADR validation | Can start provisional |
| P3 | Clean-room hash export procedure | `tools/hash_submission.py` | `--final` | Later |
| P3 | Examiner position on KG supersession | Architecture review | ADR-KG-001 accept | Document residual risk |

Items that keep metrics provisional do **not** downgrade framing mode from decision-ready.
