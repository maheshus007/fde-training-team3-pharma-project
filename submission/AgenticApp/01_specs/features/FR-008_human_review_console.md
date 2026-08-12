# FR-008 — Human review console

**Question this file answers:** what the reviewer sees, what the interface makes hard to do carelessly, and where its authority stops.

No fixture exercises the UI, so this feature is verified by end-to-end and accessibility tests rather than by a pack. That is also why it is a Demonstrator (`../poc_vs_production.md`).

| Field | Entry |
|---|---|
| Workflow | Shared — presents A, B and C |
| Contract | Consumes the four response contracts. **Produces none** |
| Fixtures | None. Verified by `tests/e2e/` over fixture-derived packs |
| Injects | 006, 063, 071, 072, 073, 074, 079 |
| Principles | AP-4, AP-10 |
| Owner | UX lead, with quality lead as reviewer proxy |
| Phase | 5 |
| Spec version | 1.0 |
| Lifecycle stage | **1 — Defined.** Awaiting stage 2 validation |
| Reviewer | Pending |

## 1. Actor and trigger

A qualified person, safety physician, supply governance member or auditor opens a pack produced by an earlier run.

## 2. Preconditions

A schema-valid pack exists · the viewer's role and entitlements are resolved server-side · the API is reachable. The console never reads source data directly.

## 3. Happy path

1. List packs the viewer is entitled to see.
2. Open a pack: findings, contradictions, gaps and abstentions each in their own region, none collapsed by default.
3. Every claim links to its evidence item, showing source, authority, effective date, retrieval time and hash.
4. The reviewer opens each critical evidence item; the interface tracks which remain unopened.
5. The reviewer acknowledges, or contests with a reason.
6. The event is recorded in the audit trail and the reviewer is told, in plain words, that acknowledgement is not a signature and not a decision.

## 4. Exceptions

| Situation | Behaviour |
|---|---|
| Critical evidence not yet opened | Acknowledgement is unavailable, with the remaining items named. Not a warning that can be clicked past |
| Pack contains abstentions or gaps | Displayed at the same visual weight as findings. An unanswered question is not a footnote |
| Viewer lacks entitlement to a segment | The segment is absent from the API response, so it cannot be present in the DOM |
| Contradiction present | Both positions shown side by side with their sources. The interface offers no control that resolves one in favour of the other |
| API unavailable | A clear degraded state naming the manual runbook. No cached pack is presented as current |
| Right-to-left or non-Latin content | Rendered correctly; text direction never changes a value |

## 5. Business rules

| ID | Rule | Inject |
|---|---|---|
| **BR-064** | The console contains **no business rule**. Every value shown is computed server-side; the UI cannot derive, round, sort or reconcile anything | AP-10 |
| **BR-065** | Acknowledgement requires that every critical evidence item has been opened. The gate is functional, not advisory | 071 |
| **BR-066** | Acknowledgement is labelled in the interface as a workflow event, explicitly not an electronic signature and not a disposition | 071 |
| **BR-067** | Abstentions, gaps and contradictions are presented with equal prominence to findings, and none is collapsed by default. The interface is designed against automation bias, not for reviewer speed | 071 |
| **BR-068** | No control exists anywhere in the console that would release, reject, allocate, reserve, ship, code a case, confirm a signal or decide eligibility. The absence is verified by a route and component inventory | 006 |
| **BR-069** | Unentitled content is absent from the API payload, not hidden by CSS or client-side filtering | 063 |
| **BR-070** | The console meets WCAG 2.2 AA on the core screens and is fully keyboard operable; quality of presentation does not vary by language or script | 072, 073 |
| **BR-070a** | Where segregation of duties applies, one identity cannot both prepare and acknowledge the same pack. The conflict is detected server-side and reported, not merely hidden in the UI | 074 |

## 6. Acceptance criteria

| ID | Criterion | Verified by |
|---|---|---|
| **AC-FR008-01** | A route and component inventory shows zero controls capable of a regulated action; the test fails if a new route introduces one | `T-GATE`, INJ-006 |
| **AC-FR008-02** | The acknowledge control is disabled until every critical evidence item is opened, and the remaining items are listed by name | `T-UX`, INJ-071 |
| **AC-FR008-03** | Acknowledgement writes an audit event carrying identity, time and pack hash, and the UI text states it is not a signature | `T-UX`, `T-BEHAV` |
| **AC-FR008-04** | Abstentions, gaps and contradictions are visible without scrolling past findings and without expanding a collapsed region, on a 1280×800 viewport | `T-UX`, INJ-071 |
| **AC-FR008-05** | For a role without sensitive-segment entitlement, the segment appears nowhere in the network payload, verified by inspecting the response body rather than the DOM | `T-SEC`, INJ-063 |
| **AC-FR008-06** | Every displayed claim links to an evidence item showing source, authority, effective date, retrieval time and hash | `T-UX` |
| **AC-FR008-07** | Zero axe-core critical or serious violations on the four core screens | `T-UX`, NFR-14, INJ-073 |
| **AC-FR008-08** | Every interactive element is reachable and operable by keyboard, with a visible focus indicator | `T-UX`, NFR-14, INJ-073 |
| **AC-FR008-09** | Arabic renders right-to-left and Hindi renders correctly; the underlying values are identical to the Latin-locale render, compared as bytes | `T-UX`, NFR-15, INJ-072 |
| **AC-FR008-10** | With the API unavailable, the console shows a degraded state naming the manual runbook and presents no stale pack as current | `T-RESIL`, INJ-079 |
| **AC-FR008-11** | A contradiction renders both positions with their sources and offers no resolve control | `T-UX` |
| **AC-FR008-12** | An identity that prepared a pack cannot acknowledge it where segregation of duties applies; the refusal is enforced server-side and appears in the audit trail | `T-GATE`, INJ-074 |

## 7. AI and human boundary

The console displays model-generated text only inside clearly labelled annotation regions, visually distinct from evidence-derived content. There is no chat box that can act. The reviewer's judgement is the output of this feature; the software's job is to make an uninformed acknowledgement difficult.

## 8. Out of scope

Electronic signatures under 21 CFR Part 11 or Annex 11 · editing evidence · overriding a computed state · dashboards and analytics · notifications · mobile layouts.

## 9. Ambiguities

None blocking. "Critical evidence item" is defined by the pack itself — items cited by a blocking gap or an unresolved contradiction — so the console never decides criticality.

## 10. Specs to load when implementing

`../product/scope.md` · this file · `../data/state_transitions.md` §4 · `../api/api_contracts.md` · `../nfrs.md` NFR-14, NFR-15 · `../poc_vs_production.md`.
