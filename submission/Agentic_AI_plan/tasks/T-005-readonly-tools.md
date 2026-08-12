# T-005 — Read-only tool adapters

## Specs to load

- [`../technical/tool-gateway.md`](../technical/tool-gateway.md)
- [`../features/agent-assist-batch.md`](../features/agent-assist-batch.md)
- [`../features/agent-assist-supply.md`](../features/agent-assist-supply.md)

## Deliverable

- `aegis/agents/tools/batch_status_read.py` — fixture/read only
- `aegis/agents/tools/draft_supply_option.py` — in-memory draft text only (V-FIX-02)
- No write APIs

## Done when

- [ ] Tools callable only through gateway
- [ ] Supply tool cannot set quality status or reservations
