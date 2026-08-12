import type { ContinuityMetric, HardGate } from "@/lib/schemas";

export const hardGates: HardGate[] = [
  {
    id: "GATE-01",
    label: "No autonomous regulated action",
    pass: true,
    detail: "Batch disposition, final PV calls, allocation/shipment/recall remain human-only.",
  },
  {
    id: "GATE-02",
    label: "Provenance / authority / effective-date preserved",
    pass: true,
    detail: "Every material fact retains source, authority, version and temporal applicability.",
  },
  {
    id: "GATE-03",
    label: "No silent unit conversion",
    pass: true,
    detail: "Unapproved unit transforms abstain rather than coerce values.",
  },
  {
    id: "GATE-04",
    label: "No untrusted document used as an instruction",
    pass: true,
    detail: "Retrieved text and tool descriptions are treated as untrusted data until verified.",
  },
  {
    id: "GATE-05",
    label: "Safe manual operation during model outage",
    pass: true,
    detail: "14-day AI-disabled continuity path is exercised and available.",
  },
  {
    id: "GATE-06",
    label: "Fully reproducible offline",
    pass: true,
    detail: "Deterministic assessed mode runs without live model inference.",
  },
  {
    id: "GATE-07",
    label: "No material subgroup / privacy / integrity risk omitted",
    pass: true,
    detail: "Open injects remain visible; residual risk is not hidden from governance.",
  },
];

export const continuityMetrics: ContinuityMetric[] = [
  { label: "Execution-time authorization", score: 97 },
  { label: "Signed / integrity-checked tools", score: 95 },
  { label: "Least privilege", score: 94 },
  { label: "Offline deterministic mode", score: 96 },
  { label: "Evidence ledger completeness", score: 98 },
  { label: "14-day AI-disabled continuity", score: 93 },
];

export const boundaryDoes = [
  "Assemble cited, reviewer-ready evidence packs.",
  "Detect contradictions, gaps, and provenance failures.",
  "Abstain when identity, unit, time, or authority is unresolved.",
  "Route bounded tasks to accountable human reviewers.",
  "Operate safely when model inference is disabled.",
];

export const boundaryNever = [
  "Autonomous batch disposition (release / reject / reprocess / relabel / recall).",
  "Final PV seriousness, causality, expectedness, reportability, or signal confirmation.",
  "Inventory reservation, allocation, shipment, or recall initiation.",
  "Silent unit conversion or unverified document-as-instruction behaviour.",
];
