# SRS — Pre-build traceability (Prompt 08 §G) + gap audit (§H2)

## G. Matrix

| Feature | Contract | BRs | ACs | ADR-AA | Ambiguity |
|---|---|---|---|---|---|
| FR-A | `submit_workflow` batch_evidence → `batch_response.schema.json` | BR-A1..A5 | AC-A1..A7 | 001,003,011,014 | conflicted_evidence rule **assumed** (STATE_TRANSITIONS) |
| FR-B | `submit_workflow` pv_intake → `pv_response.schema.json` | BR-B1..B4 | AC-B1..B9 | 001,003,013 | duplicate: return all CSV pairs; no extra cutoff **assumed** |
| FR-C | `submit_workflow` supply_options → `supply_response.schema.json` | BR-C1..C3 | AC-C1..C5 | 006,012 | option rank explainable or unmarked rank **assumed** |
| FR-D | Orchestrator + ErrorEnvelope | BR-D1..D5 | AC-D1..D5 | 002,005,007,009,016 | budgets 20/30/3 **assumed** until artefact 23 |
| FR-E | `query_graph` CQ-1..9 + GraphPort | BR-E1..E4 | AC-E1..E5 | 015,018,011,013 | default graph = assessment port **resolved** |
| FR-F | Taipy + `ack_human_review` | BR-F1..F2 | AC-F1..F3 | 008,017 | WCAG level Unknown; keyboard min **assumed** |

## H2. Orphan / gap audit

| Gap type | Finding | Disposition |
|---|---|---|
| FR without AC | None for FR-A..F | OK |
| BR without AC | BR-D5 purpose limitation covered by AEGIS-401 | fixed in SRS |
| AC without contract | AC-F3 a11y — no API; NFR-not-numeric | **assumed** keyboard tab order on 4 pages; revisit Prompt 12 |
| Endpoint without FR | `health` | allowed infra; not a product FR |
| Matching without number | PV duplicates | **assumed** no cutoff (all fixture rows); merge forbidden |
| Error envelope without AC | AEGIS-401/422/412 | AC-D2, AC-A4/B5/C3, AC-F1 |
| AC-A6 OOS | contradiction.kind=`oos_status` | INTERNAL_OBJECT_SHAPES §2–3 |
| AC-A7 QP gap | gap.kind=`supplier_audit_commitment` | §2 |
| AC-B3..B9 | clock/listedness/MedDRA/sensitive/authenticity shapes | §4 |
| AC-C5 channels | constraints.channel enum | §5 |
| AC-D1 tools | allowlisted names + manifest hash | §7 |
| AC-D3 checkpoint | resume_checkpoint_id | §8 |
| AC-E2 CQ-2 | GraphPort CQ-2 params | §6 |
| Endpoint ingest_graph | FR-E ingest | allowed |

No unmarked orphans for the in-scope build path. Gap audit **also copied** to `submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md` (Prompt 08 H2).
