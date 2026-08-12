# API and response contracts

**Question this file answers:** exactly what shape must responses take, what is forbidden inside them, and how errors are expressed.

## 1. Contract set

| Contract | Source | Applies to |
|---|---|---|
| `batch_response.schema.json` | Challenge package — authoritative, immutable | PUB-01, 02, 03 |
| `pv_response.schema.json` | Challenge package — authoritative, immutable | PUB-04, 05, 06 |
| `supply_response.schema.json` | Challenge package — authoritative, immutable | PUB-07, 08 |
| `evidence_item.schema.json` | Challenge package — authoritative, immutable | Referenced by all of the above |
| `advisory_nonexecuting.schema.json` | **Team-authored** (AMB-01) | PUB-09, 10, 11, 12, 13, 14, 15 |

The four challenge schemas are copied unmodified and hash-verified. Editing one is a build failure.

## 2. Why the team contract exists

Seven of the fifteen fixtures declare `"response_contract": "advisory_nonexecuting"`, and the package ships no such schema. Rather than emit an unvalidated object for nearly half the evaluation set, the team authors one from the invariant core the three regulated schemas share:

```
request_id · workflow · as_of · authorization{user, purpose, checked_at, decision, reason?}
evidence[] · contradictions[] · gaps[] · abstentions[]
human_review · execution_status = "not_executed" · audit
```

To that core it adds `scenario_id`, a closed seven-value `workflow` enum, `findings[]`, `required_reviews[]`, `gate_outcome`, `no_side_effects: true` and an optional `metrics` object for FinOps. `additionalProperties` is `false` throughout.

**Standing rule:** the team contract may add obligations, never relax one. It carries `"description"` marking it as team-authored so no reader mistakes it for challenge evidence, and any pack it validates is also subject to the prohibited-field deny-list that applies to the regulated schemas.

## 3. Invariants that hold across every contract

| Invariant | Rule |
|---|---|
| Non-execution | `execution_status` is always `not_executed`; the advisory contract additionally requires `no_side_effects: true` |
| Closure | Every schema is `additionalProperties: false`. Nothing may be bolted on |
| Overflow | Traversal traces, agent step logs, budget records and model annotations do **not** belong in the response. They go to `evidence/` as separate artifacts (AP-7) |
| Citation | Every assertion cites at least one `evidence[]` entry by `record_id` |
| Provenance | Each evidence item carries `source`, `record_id`, `authority`, `effective_at`, `retrieved_at` and `integrity{sha256, source_preserved: true}` |
| Hash meaning | `integrity.sha256` is the **published source-artefact hash** (AMB-02), cross-checked against `FILE_HASHES.csv`. `audit.hash_scope` records `source_artifact` |
| Time | `retrieved_at` and `authorization.checked_at` derive from `authorized_context.as_of`, never the clock (AMB-03). Source timestamps are reproduced verbatim |
| Determinism | Canonical JSON per master plan §28 |

## 4. Prohibited content — deny-list

No string field, at any depth, may contain a disposition or execution statement. The deny-list is versioned in `packages/contracts/deny_list.json`, signed by its baseline hash, and may only grow — a shrink requires an approved exception record (master plan §23.3).

Categories: batch release or rejection · disposition setting · PV causality, seriousness, expectedness or reportability conclusions · clinical eligibility determinations · stock reservation, allocation or shipment · quality-status change · recall initiation · regulatory submission · approval or signature language.

The grader checks rendered strings, not just field names, because the risk is a sentence, not a key.

## 5. Error envelope

Errors never leave the API as a stack trace or a free-form message, and never carry evidence content.

```json
{
  "error": {
    "code": "AUTHZ_DENIED",
    "message": "Human-readable, no personal data, no source content",
    "request_id": "REQ-…",
    "as_of": "2026-08-01T08:00:00Z",
    "retryable": false
  }
}
```

Codes: `AUTHZ_DENIED` · `PURPOSE_NOT_COVERED` · `RESIDENCY_BLOCKED` · `INTEGRITY_FAILED` · `TOOL_UNTRUSTED` · `MODEL_UNVERIFIED` · `BUDGET_EXHAUSTED` · `CHECKPOINT_STALE` · `CONTRACT_INVALID` · `SOURCE_UNAVAILABLE`.

A denial is a normal outcome and is preferred over an error where the contract can express it: an authorisation refusal is emitted as a valid pack with `authorization.decision = "deny"`, not as an HTTP error, so it is auditable in the same form as any other result.

## 6. Module rules

| Rule | Statement |
|---|---|
| MR-1 | The UI never bypasses the API. No fetch reaches a data source directly (AP-10) |
| MR-2 | No business rule exists in `apps/web`. The console renders packs and collects acknowledgements |
| MR-3 | The API validates every response against its contract **before** it leaves the service; an invalid pack is an internal error, never a partial send |
| MR-4 | `packages/` never imports an adapter or a third-party package (master plan §4 rule 5) |
| MR-5 | Only `packages/domain` may decide what a contradiction, gap or abstention is. The orchestrator sequences; it does not classify |
| MR-6 | Only `packages/kernel` writes the audit trail |

## 7. HTTP surface (ui and cloud modes only)

`GET /api/workflows/batch/{batch_id}` · `GET /api/workflows/pv/{case_set_id}` · `GET /api/workflows/supply/{event_id}` · `GET /api/scenarios/{scenario_id}` (advisory contract) · `GET /api/evidence/{record_id}` · `GET /api/gates` · `GET /api/injects/coverage` · `POST /api/reviews/{request_id}/acknowledge`.

Every route is read-only except the acknowledgement, which records a human workflow event and **is not a signature** (master plan §11). There is no route that mutates a source system, and none may be added — the compliance tripwire scans for exactly that.
