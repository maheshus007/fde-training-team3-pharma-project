# T-008 — Contract tests for assist envelopes

## Specs to load

- [`../technical/agent-request-response.md`](../technical/agent-request-response.md)
- Existing prohibited-action / workflow contract tests

## Deliverable

- Tests that `core` still validates via `validate_workflow_response`
- Negatives: prohibited fields in `core` still fail
- Assist envelope fixtures under `submission/tests/fixtures/`

## Done when

- [ ] Positive batch/pv/supply envelopes pass
- [ ] Prohibited-field negatives still fail closed
