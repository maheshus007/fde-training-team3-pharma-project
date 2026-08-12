# Feature — Tool Authorization Gateway

**Question this file answers:** What should tool authorization do?

| Field | Entry |
|---|---|
| Feature ID | F4 |
| Version / date | 1.0 / 2026-08-12 |
| Injects | INJ-066, INJ-067 |

## Actor

Control plane (invoked on every agent tool call).

## Preconditions

- Tool manifest presented with `sha256` / `hash`.
- Approved hash set loaded for assessed mode.
- Current user, purpose, object, role available for re-check.

## Happy path

1. Re-check entitlement freshness (deny if stale/ambiguous).
2. Verify tool hash ∈ approved set.
3. Require `signed: true` or non-empty `signature`.
4. Deny write-like permissions, `side_effects: true`, mutating `postAction`, prohibited `hidden_default`.
5. Check tool_id allowed for current workflow purpose.
6. Allow read/draft-only execution; append trajectory step with `side_effect: false`.

## Seed catalog (assessed)

| tool_id | Stance | Notes |
|---|---|---|
| `batch_status_read` | Allow if approved hash/sign | Read batch status only |
| `draft_supply_option` | Allow if approved | In-memory draft option text only |
| `batch_status_plus` / poisoned manifest | Deny | See `submission/tests/fixtures/tool_manifest_poisoned.json` |

## Exceptions

| Case | Error code |
|---|---|
| Hash not approved | `TOOL_HASH_DENIED` |
| Unsigned | `TOOL_UNSIGNED` |
| Write/disposition permission | `TOOL_WRITE_DENIED` |
| Stale entitlement | `AUTHZ_STALE` |
| Purpose mismatch | `PURPOSE_DENIED` |

## Acceptance criteria

- [ ] Poisoned fixture denied by `check_tool_manifest`
- [ ] Every tool call re-checks authZ
- [ ] No tool executes without gateway allow
- [ ] Denied attempts audited
