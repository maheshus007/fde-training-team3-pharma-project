# M-006 — Retarget scripts and graders

## Specs to load

- [`../technical/file-migration-map.md`](../technical/file-migration-map.md)

## Deliverable

Update:

- `submission/scripts/test.py` — ensure `submission/src` on path for `aegis`
- `submission/scripts/evaluate.py`
- `submission/scripts/generate_phase2_to4.py` (`from src.*` blocks)
- Graders: `schema_grader.py`, `security_grader.py`, `prohibited_action_grader.py`, `test_graders.py`

Replace bare `contracts` / `policy_guard` imports that assumed flat `src` layout with `aegis.shared.*`.

## Done when

- [ ] Grep checklist in MT4 clean for code (exclude modular-specs docs)
- [ ] Grader unit tests still discoverable
