# INCIDENT — fail-closed response

## Classification

| Symptom | Code / behaviour | Action |
|---|---|---|
| Stale or revoked entitlement | AEGIS-401 | Do not use cached allow; re-check fixtures; deny |
| Purpose / object mismatch | AEGIS-401 | Correct purpose enum; never widen |
| Poisoned or unsigned tool | AEGIS-401 | Treat retrieved tool text as data; do not execute |
| Prohibited field or forbidden Gremlin label | AEGIS-422 | Fail closed; no partial illegal pack |
| Idempotency key reuse, different payload | AEGIS-409 | Do not overwrite prior pack |
| HITL ack without viewing conflicts | AEGIS-412 | Force evidence viewing |
| Unknown CQ | AEGIS-404 | Do not invent graph paths |
| Cosmos down and `AEGIS_GRAPH_FALLBACK=false` | AEGIS-504 retryable | Enable fallback or use assessment memory port |
| Model hash mismatch (INJ-070) | inference stub `used=false` | Continue rules path |

## Kill switch

Set `AEGIS_KILL_SWITCH=true` or request `kill_switch=true`. Inference adapter is disabled; rules, graph memory, and HITL stay up (ADR-AA-002).

## What not to do

Do not bypass `policy_guard`. Do not add forbidden edges (`RESERVED_FOR`, `CASE_MERGED`, `DISPOSITION_SET`, …). Do not retry Azure on invalid JSON. Do not use AEGIS-429 on `submit_workflow`.

## Evidence

Correlate with `request_id` and audit sidecars under `submission/evidence/audit/`. Redact any `sk-` or `key=` patterns from logs.
