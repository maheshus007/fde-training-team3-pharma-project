# SRS addendum — Internal JSON shapes (Prompt 08 gap closure)

Package schemas leave `contradictions[]`, `gaps[]`, `abstentions[]`, `human_review`, `audit`, and PV/supply nested arrays as generic `object`. Team 3 **runtime MUST** emit the shapes below so builders do not invent fields. Extra keys on those nested objects are allowed by package schema but **forbidden by Team 3** (`additionalProperties` conceptually false). If a key is not listed, do not emit it.

`as_of` / `checked_at` / `retrieved_at`: ISO-8601; **`Z` suffix allowed** (same as `evaluation/contract_samples`, e.g. `2026-08-01T08:00:00Z`).

---

## 1. WorkflowRequest (input; not a package schema)

`additionalProperties: false` at root.

```
request_id: string minLength 1
idempotency_key: string minLength 8
workflow: batch_evidence | pv_intake | supply_options
as_of: string ISO-8601
authorization: {
  user: string
  purpose: batch_review_readiness | pv_intake | supply_options
  object_id: string
  role: string   // e.g. qp_reviewer | pv_assessor | supply_planner | auditor
}
batch_id?: string          // required if workflow=batch_evidence
case_ids?: string[]        // required if pv_intake, minItems 1
event_id?: string          // required if supply_options
kill_switch?: boolean      // default false
resume_checkpoint_id?: string  // optional; AC-D3
```

No `runtime_mode` on request if it would leak into logs as extra; **assumed:** mode is **env only** (`AEGIS_RUNTIME_MODE`). Request field `runtime_mode` from v1 SRS is **withdrawn** so clients cannot override assessment default. Revisit: none.

---

## 2. Shared nested objects (inside success responses)

### contradiction

```
id: string   // format {kind}:{left}:{right}  e.g. genealogy:MES|SUA-88:WM-90|SUA-88
kind: genealogy | unit | oos_status | idmp | listedness | clock | logger_pallet | other
left: { source, record_id, verbatim }
right: { source, record_id, verbatim }
```

HITL `viewed_conflict_ids` must equal these `id` values (AC-F1).

### gap

```
id: string
kind: string   // e.g. supplier_audit_commitment | missing_document
record_ref: string
note: string
```

AC-A7: INJ-028 → `kind=supplier_audit_commitment`.

### abstention

```
code: unit_unapproved | identity_unresolved | time_unresolved | authority_unresolved | trust_untrusted | authenticity_failed | budget_exhausted | graph_degraded | other
reason: string
record_ref: string | null
```

AC-A3: LR-88 → `code=unit_unapproved`.  
AC-B9: social unauthenticated → `authenticity_failed`.

### human_review (matches golden samples)

```
required: boolean
role: string
```

Do not add `acknowledged` into this object on the **workflow response** (package samples only have required+role). Ack lives in audit store only.

### audit (package requires object; samples use event_id)

```
event_id: string
```

Internal replay flag **not** in this object (would be extra). Store `replay` in `submission/evidence/audit/` sidecar only.

---

## 3. Batch-only internals

`applicable_documents[]` items:

```
doc_id: string
source: string
status: string    // catalog status
```

OOS disagreement (AC-A6): one `contradiction` with `kind=oos_status` and left/right verbatim statuses from LIMS vs statistical vs notebook.

---

## 4. PV nested items

### duplicate_candidates[] (AC-B2)

```
case_id_a: string
case_id_b: string
similarity: number   // from CSV as-is; 0.71 and 0.93 are valid examples
reason: string
```

No merge field. Include PV-1009 when in request or linked by CSV.

### clock_evidence[] (AC-B3)

```
case_id: string
channel: string    // vendor | affiliate | global
timestamp: string  // as sourced
timezone: string | "timezone_unknown"
```

### terminology[] (AC-B7)

```
case_id: string
verbatim: string
pt: string
meddra_version: string   // e.g. "27.1" | "28.0"
```

### listedness_context[] (AC-B4)

```
product_id: string
risk: string
source_doc: string    // IB | CCDS | local_label
jurisdiction: string
listed: "yes" | "no" | "unknown"
effective_at: string | null
```

### source_facts[]

```
case_id: string
pointer: string     // verbatim pointer / field name
value: string
```

Sensitive segments (AC-B8): if `authorization.role` not in `{pv_assessor, pv_medical, auditor_elevated}`, omit pregnancy/paediatric `source_facts` rows tagged `sensitive=true` inside `value` prefix `[sensitive]`. Do not add a `sensitive` key if it risks schema issues — encode in `pointer`=`narrative_redacted`.

**Assumed:** `required_reviews[]` includes `"safety physician"` when duplicates or clock conflicts exist.

---

## 5. Supply nested items

### options[]

Package requires `option_id` + `status=draft`. Team 3 MAY also emit:

```
summary: string
constraint_ids: string[]
```

MUST NOT emit `reservation_id`, `allocation_id`, `shipment_id`.

### constraints[] (AC-C5)

```
constraint_id: string
channel: commercial | trial | compassionate | other
note: string
```

### quality_holds[]

```
batch_id_or_lot: string
status: string   // source string e.g. quality_hold
```

---

## 6. GraphQueryResult

```
cq_id: string
paths: [ { nodes: string[], edges: string[], provenance: object[] } ]
abstentions: [ { code, reason } ]
truncated: boolean
```

`paths` max length **50**; if more, set `truncated=true` (token/context cap).

### CQ params

| cq_id | params (required keys) |
|---|---|
| CQ-1 | `batch_id` |
| CQ-2 | `lab_result_id` (e.g. `LR-88`) |
| CQ-3 | `case_ids` string[] |
| CQ-4 | `product_id`, `risk` |
| CQ-5 | `product_id_a`, `product_id_b` |
| CQ-6 | `shipment_id` |
| CQ-7 | `event_id` |
| CQ-8 | `manifest_id` |
| CQ-9 | `user`, `purpose`, `object_id` |

IDMP match order (FR-E): **exact id → alias table → stop**. Never fuzzy-equate. CQ-5 returns conflict, not merge.

---

## 7. Tool catalog (FR-D / AC-D1)

File: `submission/tests/fixtures/tool_manifest_approved.json` (and poisoned variant).

Runtime loads **only** tools in approved manifest whose `hash` matches file sha256. Allowed tool names:

`resolve_concept`, `get_provenance`, `find_conflicts`, `traverse_evidence_path`, `assess_readiness`, `propose_duplicate_candidates`, `enumerate_draft_options`, `request_human_review`

No other tool names. Poisoned manifest → AEGIS-401/422 deny before any tool call.

---

## 8. Checkpoint (AC-D3)

`resume_checkpoint_id` on WorkflowRequest loads `submission/evidence/checkpoints/{id}.json`.

Checkpoint body:

```
checkpoint_id, request_hash, step, tool_calls_used, inference_calls_used, partial_facts_hash, termination_reason: null | budget | kill_switch | completed
```

Resume MUST NOT duplicate audit `event_id`; append `resume_of`.

---

## 9. Auth deny vs budget stop

| Condition | Client result |
|---|---|
| Auth deny / poisoned tool | **ErrorEnvelope** AEGIS-401 or 422 — no workflow success body |
| Budget stop after some rules ran | **Success** schema-valid pack + abstention `budget_exhausted` (HTTP 200). AEGIS-429 envelope **not** used for `submit_workflow` |
| Schema/prohibited on output | Fail closed ErrorEnvelope AEGIS-422; do not return partial illegal JSON |

This supersedes the earlier “429 on budget” for `submit_workflow`.
