# SRS — Data model and graph schema (Prompt 08)

## 1. Identity and time

| Concept | Rule |
|---|---|
| Identifiers | Preserve source string; namespace as `{system}|{id}` in graph `id` property, e.g. `MES|SUA-88` |
| `as_of` | Filter edges where `effective_at` is null **or** `effective_at` ≤ `as_of` |
| `effective_at` | ISO-8601 or null; null ⇒ cannot support time-critical claims without abstention |
| `retrieved_at` | Set at ingest/query time (ISO-8601) |
| Timezone | Store source tz or `timezone_unknown`; never coerce to UTC without `timezone_rules` applicability |

## 2. EvidenceFact (logical / RER)

Columns: `source`, `record_id`, `authority`, `effective_at`, `retrieved_at`, `facts` (JSON), `integrity.sha256`, `integrity.source_preserved=true`, `trust_status` (`trusted`\|`untrusted`\|`draft`\|`superseded`\|`unknown`), `purpose_scope`.

Untrusted facts may be listed as evidence of “document exists” but **must not** drive tool policy.

## 3. Cosmos Gremlin / in-memory graph

Partition key property: `pk` (string). POC value = vertex `label`.

### Vertex labels (allowed)

`Batch`, `MaterialLot`, `LabResult`, `IcsrCase`, `Product`, `Shipment`, `Logger`, `Pallet`, `Document`, `Mapping`, `EvidenceFact`, `Constraint`, `InventoryPosition`, `Organisation`

Required vertex properties: `id`, `pk`, `source_system`, `record_id`, `authority`, `effective_at`, `retrieved_at`, `integrity_sha256`, `trust_status`

### Edge labels (allowed ingest)

`CONSUMED`, `MISSING_BRANCH`, `ISSUED`, `CODED_AS`, `LISTED_IN`, `NOT_LISTED_IN`, `ALIASED_AS`, `ASSOCIATED_LOGGER`, `ASSOCIATED_PALLET`, `DUPLICATE_CANDIDATE`, `CONSTRAINED_BY`, `EVIDENCED_BY`, `MAPPED_TO`

Required edge properties: same provenance set + `ingest_batch_id`

`DUPLICATE_CANDIDATE` may include `similarity` number from CSV (e.g. 0.93, 0.71) — **display only; never merge**.

### Edge labels (forbidden — GraphPort MUST reject addE)

`RESERVED_FOR`, `ALLOCATED_TO`, `SHIPPED_AS`, `DISPOSITION_SET`, `QUALITY_STATUS_CHANGED`, `SIGNAL_CONFIRMED`, `CASE_MERGED`, `ELIGIBILITY_DETERMINED`

## 4. What must never be written back to SoR

LIMS, MES, QMS, safety DB, inventory, IAM. Graph ingest is from challenge CSV/fixtures only (copy into graph), not a write to NovaCura systems.

## 5. Local stores (assessment)

| Store | Path | Contents |
|---|---|---|
| Idempotency | `submission/evidence/idempotency/` | key → response hash + body |
| Checkpoints | `submission/evidence/checkpoints/` | AgentRun JSON |
| Audit append | `submission/evidence/audit/` | one JSON object per line or file per request |

Reset script deletes these three dirs only — never `case/` or `data/`.

## 6. ACL ingest (LIMS v1 vs v2)

| LIMS contract | Unit field | Status field | Rule |
|---|---|---|---|
| v1 | `unit` | `status` | Keep verbatim |
| v2 | `ucum_code` | `lifecycleState` | Keep verbatim; do not rename into v1 keys in `facts` |

Store `contract_version` inside `facts.contract_version`. Conversion only if `interface_mappings.approved=yes` for that pair.

## 7. Integrity hash

`integrity.sha256` = lowercase hex SHA-256 of UTF-8 canonical JSON of `facts` (keys sorted, no extra whitespace). Empty `facts` `{}` hashes to a stable value; golden samples using 64 zeros are **package samples only** — runtime packs MUST use the real hash.

## 8. Entitlement records

Read `submission/tests/fixtures/users_entitlements.json` and `access_cache_stale.json` (and package `data/` equivalents when wired). Freshness: `iam_state` in `{active, enabled, allow}`; `revoked_at` not ≤ `as_of`; `cached_until` not < `as_of` (existing `policy_guard.check_authorization_records`).
