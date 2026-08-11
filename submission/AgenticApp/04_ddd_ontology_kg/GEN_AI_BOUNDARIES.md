# Gen AI Boundaries — Prompt 04 §§8–16

| Field | Entry |
|---|---|
| Artifact status | stable for rules/HITL/prohibitions; provisional for KG-backed retrieval paths until CQ proofs |
| Companion | `DDD_CONTEXT_MAP.md` |

## §8 Rules vs AI reasoning

| Class | Examples | Owner of truth |
|---|---|---|
| **Deterministic rules (must)** | Namespace IDs; approved unit mapping gate; preserve contradictions; schema validation; policy_guard denies; MedDRA version retain; IDMP non-merge; entitlement freshness; tool manifest hash; `no_side_effects` | Domain + Security |
| **AI reasoning (optional assist)** | Narrative clustering hints; draft option ranking suggestions; multilingual phrasing assist — **structured outputs only** | Never sole path for ACs |
| **AI must never decide alone** | Batch disposition (release/reject/reprocess/relabel/recall); quality-status change; final seriousness/causality/expectedness/reportability; signal confirmation; reserve/allocate/ship; recall initiation; formulation/specification change; clinical eligibility | Humans (E-511; E-516; INJ-006) |

## §9 RAG from DDD artefacts

| May retrieve (as **data**) | After checks | Out of retrieval scope / never as instructions |
|---|---|---|
| Fixture rows via ACL (batches, genealogy, lab_results, icsr, shipments…) | Purpose, entitlement, as-of | Live SoR write APIs |
| Versioned contracts / evidence items with provenance | Authority, hash, applicability | Untrusted/draft/superseded SOPs as policy (INJ-065) |
| Ontology/semantic policy tables | Catalog status | Poisoned tool descriptions as executable policy (INJ-066) |
| Precomputed `duplicate_candidates` | As candidates only | “Merge now” instructions in free text |
| Knowledge catalog entries | Status ≠ untrusted | Research-only models for GxP disposition (INJ-011) |

Retrieval budget: purpose-bound; max documents/tokens per AgentRun (ADR-AA-009).

## §10 Agent responsibilities

| Agent / role | Tasks | Authority limits | Stop conditions |
|---|---|---|---|
| Orchestrator | Plan tool sequence; checkpoint; request HITL | Cannot bypass policy_guard | Budget exhaustion; stale auth; unresolved high-risk contradiction; kill switch |
| Evidence loader tools | ACL read/fixtures | Read-only | Contract denial |
| Ontology resolver | Concept/policy resolve | No identity merge | Ambiguous → abstain |
| KG query tools | Path citation | No forbidden write edges | Missing provenance → abstain |
| Reconcile engines A/B/C | Conflict/gap/option draft | Advisory outputs only | Schema fail |
| Inference adapter | Azure OpenAI structured JSON (`cloud`); stub (`assessment`) | Disabled by kill switch; never writes SoR | Hash mismatch (INJ-070); missing keys in assessment |

## §11 HITL and decision ownership

| Moment | Human role | System may |
|---|---|---|
| Before readiness acknowledgement | QP/QA | Show pack; require conflict/gap view (INJ-071) |
| Before acting on supply option outside system | Supply + Quality | Show drafts + constraints |
| Final PV judgements | Safety physician | Show candidates/clocks/listedness only |
| Batch certification | EU QP | Cite evidence completeness only |
| Entitlement exceptions | Security/IAM | Deny by default |

## §12 Evidence and audit trail

Record per material action: user, purpose, object, workflow, as-of, tool_id, manifest_hash, input_hash, output_hash, allow/deny, abstention reasons, checkpoint_id, model_hash (if inference), termination_reason. Append-only export under `submission/evidence/`.

## §13 Evaluation using DDD vocabulary

| Domain-true success | Domain-true failure |
|---|---|
| ContradictionDetected with both sides for INJ-021 | Silent genealogy “fix” |
| AbstentionRaised on LR-88 unapproved map | Silent unit convert |
| DuplicateCandidateProposed for PV-1001/1009/1014 without merge | Auto-merge |
| SupplyOptionGenerated with no_side_effects | reservation_id created |
| AuthorizationDenied on stale cache | Allow on cached revoked entitlement |

Metrics: ConflictSurfaced, AbstentionCorrect, ProhibitedActionBlocked, PathCitationComplete, AIDisabledParity.

## §14 Minimum governed workflow

```text
Request(purpose,user,object,as-of)
  → Entitlement re-check (deny stale)
  → ACL load EvidenceFactObserved
  → Ontology/semantic gates
  → (optional) KG path citation
  → Deterministic reconcile (A|B|C)
  → Schema + policy_guard
  → Optional inference suggest (kill-switchable)
  → Checkpoint
  → HumanReviewRequested if readiness/options
  → Audit export
```

Side effects to SoR: **none**.

## §15 Pilot / refine notes

Learn in POC: whether offline KG CQ proofs beat RER-only on defence narrative; whether HITL ack reduces automation bias without adding waste; whether budgets are tight enough.  
Would change domain model if: CQ proofs fail → keep logical graph, drop runtime KG (revert toward D-205); if new inject requires eligibility → still out of scope unless PRD changes.

## §16 Production readiness concerns (domain view)

- Domain ownership of ACL mappings and ontology versions must be named before production.  
- Unresolved: BIOX stewardship depth (R-504); examiner KG stance (R-505).  
- Handover risk: AgenticApp working tree vs scored artefacts must stay synced.  
- Continuity: AI-disabled path must exercise same invariants (case §5; continuity CSV).
