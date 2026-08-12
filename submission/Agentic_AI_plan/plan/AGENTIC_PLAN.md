# Spec-Driven Agentic Plan (Validated)

| Field | Value |
|---|---|
| Version / date | 1.1 / 2026-08-12 |
| Status | Accepted (see [`VALIDATION.md`](VALIDATION.md)) |
| Scope root | `submission/` only |
| Framework | PRD → Feature specs → Technical specs → Architecture → Tasks |

## Locked decisions

1. **Prerequisite:** modular monolith `aegis/{shared,batch,pv,supply,runtime}` before `aegis.agents`.
2. **Agent stance:** one assist-only bounded loop per request; deterministic workflow core always runs first and remains authoritative.
3. **Default runtime:** `agent_mode=disabled` / kill switch engaged.
4. **Inference:** `OfflineExtractAdapter` in assessed mode; hash-pinned interface for any future model.
5. **Contract shape (V-FIX-01):** agent metadata lives in a **run envelope**, not inside package workflow response schemas.
6. **Specs location:** this `submission/specs/` tree; tasks under `tasks/`.

## Envelope (mandatory)

```json
{
  "schema_version": "aegis.agent_run/1.0",
  "runtime_mode": "ai_disabled_deterministic",
  "agent_mode": "disabled",
  "core": { },
  "agent": {
    "engaged": false,
    "trajectory": [],
    "annotations": [],
    "abstentions": []
  }
}
```

- `core` MUST validate against package `evaluation/contracts/{batch,pv,supply}_response.schema.json`.
- `agent.*` MUST NOT be merged into `core` when calling package schema validation.
- `core.execution_status` MUST remain `"not_executed"`.
- Supply `core.no_side_effects` MUST be `true`.

## Spec index

| Layer | File | Question |
|---|---|---|
| PRD | [`../product/prd.md`](../product/prd.md) | What problem? |
| Feature | [`../features/`](../features/) | What should it do? (F1–F6) |
| Technical | [`../technical/`](../technical/) | Exact behaviour (T1–T4) |
| Architecture | [`../architecture/agent-system.md`](../architecture/agent-system.md) | Where does code live? |
| Prompts | [`../prompts/`](../prompts/) | Assist prompt source |
| Tasks | [`../tasks/`](../tasks/) | Executable units T-001…T-012 |

## Implementation order

```
T-001 modular monolith
  → T-002 spec sign-off
  → T-003 tool registry
  → T-004 loop
  → T-005 read-only tools
  → T-006 offline adapter + kill switch
  → T-007 merge into envelope
  → T-008/T-009 tests
  → T-010 demo wiring
  → T-011 ADR-013/014 + C4 note
  → T-012 verify evidence
```

## Out of scope

- Multi-agent swarms; cross-workflow agent calls
- Write tools / brownfield mutations
- Live provider SDKs as assessed dependency
- Next.js dashboard rewrite
- Edits outside `submission/`

## Success criteria

- One question per spec file; tasks cite only needed specs
- Default path AI-disabled with empty trajectory
- S08 trajectory + security expectations covered by tests
- Package contract validation of `core` remains green
- No prohibited fields (INJ-006) in `core` or trajectory actions
