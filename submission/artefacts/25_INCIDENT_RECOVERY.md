# Incident and Recovery

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v1.1 — 2026-08-12 |
| Reviewers | Pending team review |
| Status | Current with runbooks |
| Related requirements / ADRs | Artefacts 16, 24; `submission/runbooks/INCIDENT.md`, `AI_DISABLED.md`; INJ-069, INJ-079, INJ-080 |

## Purpose

Defines how to detect, contain, preserve evidence, roll back and resume after AI/platform/security incidents — including events already in the challenge log. Accountable owner: CISO / Incident Commander (role-played). Completion criteria: kill-switch and evidence-preservation rules are explicit; CAPA resumption criteria do not waive failed VT items.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2501 | `data/downtime_events.csv` | Incident log | DT-1 ransomware containment; DT-2 open AI regional outage | Real scenario incidents |
| E-2502 | `data/security_events.csv` | Security log | SEC-1/SEC-2 historically unblocked | Abuse incidents |
| E-2503 | `data/agent_runs.csv` AR-77 | Agent log | Checkpoint resume duplicates | Integrity incident |
| E-2504 | `data/audit_trails.csv` / privileged_sessions | Audit evidence | Audit capture disabled during privileged overrun | Evidence-preservation failure mode |
| E-2505 | `knowledge/GXP_DATA_INTEGRITY_STANDARD.md` | Policy | Do not overwrite originals/audit evidence | Retention during incident |
| E-2506 | `submission/runbooks/INCIDENT.md`, `AI_DISABLED.md`, `OPERATIONS.md`, `SETUP.md` | Participant ops | Filed continuity / incident playbooks | Thin; drill not yet recorded |

## 1. Incident taxonomy

| Class | Examples | Severity |
|---|---|---|
| Security/abuse | SEC-1 exfil attempt, SEC-2 DoW, poisoned tool, stale auth | Sev-1/2 |
| Integrity | Model hash mismatch, checkpoint duplication, audit gap | Sev-1 |
| Availability | DT-1 OT ransomware, DT-2 AI region down | Sev-1/2 |
| Privacy | Residency breach, DSR/hold conflict mishandled, consent cache miss | Sev-1/2 |
| Safety/quality decision risk | Automation-bias unsafe accept, disposition language escape | Sev-1 |

## 2. Detection and triage

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Detect | Gate deny spikes; integrity mismatch; open downtime events; reviewer unsafe-accept signals; token anomalies | IC / Platform | E-2501, E-2502 |
| Triage questions | Patient/product impact? Regulated decision influenced? Evidence integrity intact? Side effects executed? | IC | This artefact |

## 3. Containment and kill switch

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Kill switch | Disable model inference and tool-calling immediately; leave deterministic read-only reconcile/cite paths if integrity intact; if audit/auth integrity doubtful, disable AI-EVIDENCE UI and revert to `runbooks/AI_DISABLED.md` + manual process. | CISO / CQO | E-2501, E-2504, E-2506 |
| Auth incidents | Force live-IAM only; flush gateway entitlement cache. | CISO | Artefact 12; PUB-09 |
| DoW | Enforce token cap; block offending principal. | Platform | E-2502; S11 |

## 4. Evidence preservation

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Rule | Do not overwrite logs, prompts under hold, or audit trails during remediation (E-2505). | CQO / CISO | E-2504, E-2505 |
| Capture | request_id, gate outcomes, model hashes, user, timestamps, checkpoint IDs | Platform | evaluate/run evidence shape |

## 5. Rollback and reconciliation

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| AI drafts | Drafts are non-executing — rollback = discard/mark superseded, reconcile duplicates (AR-77). | Capstone team | E-2503; PUB-13; S08/S12 |
| If side effect ever occurred | Out of assessed mode by design; escalate as quality incident / deviation — not “re-run AI.” | CQO | ai_use_boundaries |
| Demo reset | `python submission/scripts/reset.py` clears regenerable evaluation_results only; package evidence untouched. | Capstone team | E-2506 |

## 6. Communication and regulatory assessment

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Internal | IC → CQO, CISO, DPO, QP/PV/Supply as impacted | Per RACI | artefact 03 |
| Regulatory | Assess whether batch certification, PV reporting, or privacy breach notification duties triggered — case-by-case. | RA / QP / DPO | E-2501 classes |

## 7. CAPA and resumption criteria

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Resumption requires | Root cause documented; failed control fixed; regression tests green; deadline for AI inference — integrity + VT re-pass; human communications completed. | CQO | Artefact 14/21 |
| Explicit non-resumption | “Primary region still down but fallback model is up” is **not** sufficient if integrity/scope fail (artefact 24). | Platform | E-2501, E-2502 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2501 | Gap | Runbooks filed but formal timed drill result not yet recorded | Medium | Capstone / Ops | Before pilot | Open |
| R-2502 | Risk | DT-2 still open — organisation may already be in degraded mode without formal IC | High | Platform | Immediate | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Duplicate checkpoint contained | checkpoint age/idempotency | PUB-13; trajectory | E-2503 | PASS (POC) |
| Kill switch documented | This artefact + runbooks | INCIDENT / AI_DISABLED | E-2506 | PASS (doc) |
| Drill evidence | Timed continuity drill | — | R-2501 | Partial |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | CISO / IC | — | — | — |
