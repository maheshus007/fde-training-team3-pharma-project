# SRS — API / interface contracts (Prompt 08)

| Field | Entry |
|---|---|
| Status | Stable for minimum governed slice |
| Contract version | `aegis.workflow.v1` |
| Package schemas | `evaluation/contracts/*.schema.json` (immutable; responses MUST validate) |
| Auth | Execution-time entitlement from fixtures (not Azure AD in POC). Deny-by-default. |

Taipy and CLI call the **same Python service**. HTTP is optional wrapping of that service.

---

## 1. Common request (`WorkflowRequest`)

Used by `Orchestrator.submit(request)`.

| Field | Type | Rule |
|---|---|---|
| `request_id` | string | minLength 1; UUID recommended |
| `idempotency_key` | string | minLength 8; required |
| `workflow` | enum | `batch_evidence` \| `pv_intake` \| `supply_options` (**not** `supply_planning`) |
| `as_of` | string | ISO-8601; `Z` or numeric offset both allowed (fixtures use `2026-08-01T08:00:00Z`) |
| `authorization.user` | string | Must match entitlement `user_id` |
| `authorization.purpose` | string | Must be exactly one of: `batch_review_readiness`, `pv_intake`, `supply_options` |
| `authorization.object_id` | string | batch_id / case_id / event_id as applicable |
| `authorization.role` | string | `qp_reviewer` \| `pv_assessor` \| `pv_medical` \| `supply_planner` \| `auditor` \| `auditor_elevated` |
| `kill_switch` | boolean | default false; true forces inference off |
| `resume_checkpoint_id` | string | optional; AC-D3 |

Runtime mode is **env only** (`AEGIS_RUNTIME_MODE`), not a request field (clients cannot override assessment default).

Nested success-object shapes: see `INTERNAL_OBJECT_SHAPES.md` (mandatory).

### Workflow-specific required fields

| workflow | Extra required | Example values |
|---|---|---|
| `batch_evidence` | `batch_id` | `NCB204-B24071` |
| `pv_intake` | `case_ids` array minItems 1 | `["PV-1001","PV-1009","PV-1014"]` |
| `supply_options` | `event_id` | `SH-901` (cold-chain) or shortage event id from fixtures |

Purpose must match workflow:

| workflow | required purpose |
|---|---|
| batch_evidence | `batch_review_readiness` |
| pv_intake | `pv_intake` |
| supply_options | `supply_options` |

Mismatch → `AEGIS-401` purpose mismatch.

---

## 2. Common success response

Must validate against package schema for that workflow. Always:

| Field | Const / rule |
|---|---|
| `execution_status` | `not_executed` |
| `authorization.decision` | `allow` on success path |
| `authorization.checked_at` | ISO-8601 at execution |
| supply only: `no_side_effects` | `true` |
| supply options[].`status` | `draft` |

Evidence items MUST match `evidence_item.schema.json` (sha256 64 hex; `source_preserved: true`).

`idempotency_key` is **input-only** (not in package response schema). Persist internally; do not add to response (would fail `additionalProperties: false`).

---

## 3. Service operations (Python)

| Operation | Input | Success | Errors |
|---|---|---|---|
| `submit_workflow` | WorkflowRequest | Workflow response JSON | ErrorEnvelope |
| `ack_human_review` | `{request_id, user, viewed_conflict_ids[], ack: true}` | `{request_id, human_review.acknowledged: true}` stored in audit store — **does not** mutate SoR or add schema-illegal fields to the workflow response file | `AEGIS-412` if conflicts exist and `viewed_conflict_ids` incomplete |
| `query_graph` | `{purpose, as_of, cq_id, params}` | `{paths[], provenance[]}` | `AEGIS-401`, `AEGIS-404` unknown CQ |
| `health` | none | `{status, mode, inference, graph}` | none |
| `ingest_graph` | none (uses fixtures) | `{edge_count: int}` | AEGIS-422 forbidden label |
| `resume` | same as submit + `resume_checkpoint_id` | Workflow response | AEGIS-404 unknown checkpoint |

### Optional HTTP map (if CLI uses HTTP)

Base path `/v1`. Trusted local loopback only (POC). No public CORS (`CORS_ORIGINS` empty = deny browser cross-origin).

| Method | Path | Maps to |
|---|---|---|
| POST | `/v1/workflows/{workflow}/runs` | `submit_workflow` |
| POST | `/v1/reviews/{request_id}/ack` | `ack_human_review` |
| POST | `/v1/graph/cq` | `query_graph` |
| GET | `/v1/health` | `health` |

HTTP status mapping: 200 success pack; 400 schema; 401 auth deny; 409 idempotency conflict; 412 HITL ack; 422 prohibited field/label; 404 unknown CQ/checkpoint; 504 only if graph down **and** fallback disabled.

Inference unavailable: **still HTTP 200** workflow pack (rules); sidecar audit `inference_used=false`. Do not use 503 for `submit_workflow`.

Budget stop: **HTTP 200** + abstention `budget_exhausted` (see INTERNAL_OBJECT_SHAPES §9).

**Assumed:** `cloud` mode falls back to assessment GraphPort if Cosmos errors; log `graph_fallback=true`. Revisit if product forbids fallback.

---

## 4. InferencePort

```text
suggest(kind, payload: dict, budget) -> InferenceResult
```

| Field | Rule |
|---|---|
| `kind` | `cluster_hint` \| `option_rank_hint` \| `narrative_summary` |
| Output JSON | Must not contain prohibited keys (same lists as policy_guard) |
| `temperature` | **0** |
| `max_tokens` | **2048** per call |
| Max calls / AgentRun | **3** |
| Timeout | **15** seconds per call |
| Azure env | `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_VERSION` (default `2024-10-21`) |

`assessment` / `ai_disabled` / kill_switch / missing keys / hash mismatch → stub returns `{used: false, suggestions: []}` in **≤50 ms**. Workflow still completes via rules.

---

## 5. GraphPort

```text
ingest_from_fixtures() -> int  # edge count
query(cq_id, params, purpose, as_of) -> GraphQueryResult
```

Allowed `cq_id`: `CQ-1` … `CQ-9` only. Params and result shape: `INTERNAL_OBJECT_SHAPES.md` §6. Max **50** paths.

| CQ | Query intent |
|---|---|
| CQ-1 | `Batch` `NCB204-B24071` — `MISSING_BRANCH` / `ISSUED` / `CONSUMED` → `MaterialLot` (SUA-88) |
| CQ-2 | `LabResult` `LR-88` → `MAPPED_TO`; if mapping not approved → abstain unit |
| CQ-3 | `IcsrCase` PV-1001 / PV-1009 / PV-1014 `DUPLICATE_CANDIDATE` |
| CQ-4 | Product–listedness `LISTED_IN` / `NOT_LISTED_IN` by jurisdiction |
| CQ-5 | `MAPPED_TO` between NCB-204 and NCB204-DE; status ambiguous |
| CQ-6 | `Shipment` SH-901 — `ASSOCIATED_LOGGER` LG-31 — `ASSOCIATED_PALLET` P-88 and P-89 |
| CQ-7 | `CONSTRAINED_BY` on inventory/MA/ethics for event |
| CQ-8 | ToolManifest hash vs approved file |
| CQ-9 | Entitlement freshness for user/purpose/object |

Forbidden: any `addE` of labels in § forbidden list (DATA_MODEL).

---

## 6. Taipy pages (UI contract, not HTML)

| Page | Calls | Forbidden UI |
|---|---|---|
| `page_batch` | submit `batch_evidence` | Release/reject buttons |
| `page_pv` | submit `pv_intake` | Confirm signal / final causality |
| `page_supply` | submit `supply_options` | Reserve/allocate/ship |
| `page_review` | ack_human_review | Ack enabled only if all contradiction ids viewed |

---

## 7. Idempotency

Key = `idempotency_key` + `workflow` + `as_of` + `user` + canonical JSON of object ids.

- Same key + same payload hash → return stored response; audit `replay=true`  
- Same key + different hash → `AEGIS-409`  
- TTL **24 hours** (86400 s) in local store `submission/evidence/idempotency/` (assessment)
