# SRS — Non-functional requirements (Prompt 08)

Measurable only.

| ID | NFR | Target | Applies |
|---|---|---|---|
| NFR-01 | Assessment `submit_workflow` P95 without inference | **≤ 5000 ms** on workshop laptop | assessment |
| NFR-02 | Inference call timeout | **15 s** then stub/fallback | cloud |
| NFR-03 | Max agent steps / run | **20** | all |
| NFR-04 | Max tool calls / run | **30** | all |
| NFR-05 | Max Azure OpenAI calls / run | **3** | cloud |
| NFR-06 | Max tokens / inference call | **2048** | cloud |
| NFR-07 | Temperature | **0** | cloud |
| NFR-08 | Idempotency TTL | **86400 s** | all |
| NFR-09 | Assessment tests | `python submission/scripts/test.py` exit 0 **without** Azure env vars | CI |
| NFR-10 | Schema validation | 100% of successful responses validate package schemas | all |
| NFR-11 | Prohibited-action rate | **0** successful prohibited fields in automated suites | all |
| NFR-12 | Health | `GET /v1/health` or `health()` returns in **≤ 200 ms** | all |
| NFR-13 | Audit | every submit writes ≥1 audit record | all |
| NFR-14 | Kill switch | inference_used false within same request when kill_switch true | all |
| NFR-15 | Graph query CQ-1/3/6 assessment | **≤ 2000 ms** after ingest | assessment |
| NFR-16 | Secrets | zero secret files under `submission/` in git | all |
| NFR-17 | Graph paths returned | **≤ 50**; `truncated=true` if capped | FR-E |
| NFR-18 | Azure OpenAI retries | **0** by default; max **1** extra on 408/429 after 1000 ms | cloud |
| NFR-19 | Taipy bind | `127.0.0.1` only | FR-F |
| NFR-20 | sha256 | UTF-8 SHA-256 of canonical JSON `facts` object (sorted keys) | evidence items |

BR-01 cycle time −14%: **Unknown** — not an NFR for this POC.
