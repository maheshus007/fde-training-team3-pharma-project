# Tech stack decision — AEGIS AgenticApp

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Status | **Product stack accepted**; assessment/mock path mandatory |
| Owner | Architecture + Build |

## 1. What was decided

The **intended product stack** (cloud-primary, agentic) is:

| Layer | Choice | ADR |
|---|---|---|
| LLM | **Azure OpenAI** (chat + structured JSON out) | ADR-AA-016 |
| UI / HITL workbench | **Taipy** | ADR-AA-017 |
| Knowledge graph | **Azure Cosmos DB (Gremlin API)** | ADR-AA-018 / updates ADR-AA-015 |
| Domain engines, policy, contracts | **Python** under `submission/src` | ADR-AA-001 |
| Orchestrator | **LangGraph** StateGraph (allowlisted tools + Azure JSON node); engines remain SoT | ADR-AA-009 / ADR-AA-019 |

This **replaces** the previous “stdlib-only / SQLite / static `submission/app`” as the *product* target. It does **not** delete the package requirement for a runnable assessment mode without cloud keys.

## 2. Dual-mode (non-negotiable for scoring)

The capstone **cannot** be cloud-only. Hard gates require: offline or mocked execution, no secrets in the ZIP, AI-disabled continuity, reproducible tests.

| Mode | When | LLM | Graph | UI |
|---|---|---|---|---|
| **`cloud`** (product) | Local demo with credentials | Azure OpenAI | Cosmos Gremlin | Taipy |
| **`assessment`** (default for `--final` / CI) | No keys, examiner machine | Stub inference adapter | In-memory/RER graph port | Taipy against mock services **or** CLI pack export |
| **`ai_disabled`** | Kill switch / outage | Off | Read-only graph port (mock or Cosmos read) | Taipy still shows rule packs |

`AEGIS_RUNTIME_MODE=assessment|cloud|ai_disabled` (env). Default = **`assessment`**.

## 3. Ports (so cloud is swappable)

| Port | Cloud adapter | Assessment adapter |
|---|---|---|
| `InferencePort` | Azure OpenAI client | Fixture / deterministic stub |
| `GraphPort` | Cosmos Gremlin | In-memory property graph built from CSV |
| `Workbench` | Taipy pages | Same Taipy pages bound to mock API |

Engines **must not** import Azure SDKs directly. Only adapters do.

## 4. Secrets

- Never commit keys, connection strings, or `.env` with secrets.  
- Document names only, e.g. `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`, `COSMOS_GREMLIN_ENDPOINT`, `COSMOS_GREMLIN_KEY`, `COSMOS_GREMLIN_DATABASE`, `COSMOS_GREMLIN_GRAPH`.  
- Assessment mode must start with **zero** of these set.

## 5. Still forbidden (unchanged)

No autonomous disposition, final PV, allocate/ship/recall, eligibility, formulation/spec change. Gremlin **must not** persist `RESERVED_FOR` / `DISPOSITION_SET` / `SIGNAL_CONFIRMED` write edges from the agent.

## 6. Dependencies (expected; lock in Prompt 08 / requirements file)

Product extras (not required for assessment if mocked): Azure OpenAI SDK, Gremlin Python client, Taipy.  
Assessment: existing stdlib tests must still pass without those services.
