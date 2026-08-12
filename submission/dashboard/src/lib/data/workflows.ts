import { workflowSchema, type OperatingProperty, type Workflow } from "@/lib/schemas";

const propertyDefinitions = [
  ["evidence-integrity", "Evidence integrity"], ["source-authority", "Source authority"],
  ["traceability", "Traceability"], ["reproducibility", "Reproducibility"],
  ["human-oversight", "Human oversight"], ["safety-guardrails", "Safety guardrails"],
  ["privacy-controls", "Privacy controls"], ["security-controls", "Security controls"],
  ["reliability", "Reliability"], ["observability", "Observability"],
  ["cost-control", "Cost control"], ["change-control", "Change control"],
  ["ai-continuity", "AI-disabled continuity"], ["recovery-readiness", "Recovery readiness"],
] as const;

function operatingProperties(offset: number): OperatingProperty[] {
  return propertyDefinitions.map(([key, label], index) => ({
    key, label, score: Math.min(99, 87 + ((index * 5 + offset) % 12)),
  }));
}

function workflow(input: Workflow): Workflow {
  return workflowSchema.parse(input);
}

export const workflows: Workflow[] = [
  workflow({
    id: "batch", name: "Batch Evidence Triage",
    supports: ["Assemble cited batch-review evidence", "Route incomplete records to quality review", "Produce a bounded evidence summary"],
    neverDoes: ["Disposition a batch", "Change quality status", "Release material or initiate recall"],
    contractsPassing: 96, operatingProperties: operatingProperties(1),
    tracker: ["pass", "pass", "abstain", "pass", "blocked", "pass"],
    evidenceByArea: [
      { area: "Batch record", complete: 97, gap: 2, contradiction: 0 },
      { area: "LIMS results", complete: 93, gap: 4, contradiction: 1 },
      { area: "Deviation evidence", complete: 89, gap: 5, contradiction: 2 },
    ],
    contractTests: [
      { id: "BAT-P-01", name: "Cites authoritative batch evidence", kind: "positive", result: "pass" },
      { id: "BAT-P-02", name: "Creates reviewer-ready evidence pack", kind: "positive", result: "pass" },
      { id: "BAT-X-01", name: "Cannot disposition a batch", kind: "prohibited", result: "blocked" },
    ],
    sampleOutput: {
      cited: ["LIMS assay result LIMS-9821", "Executed batch record BPR-204-118"],
      contradictions: ["Assay timestamp differs from export timestamp by 60 minutes"],
      gaps: ["Signed deviation closure is pending"],
      humanReviews: ["Quality reviewer must assess disposition eligibility"],
    },
  }),
  workflow({
    id: "pv", name: "PV Case Prioritisation",
    supports: ["Identify evidence-backed case signals", "Surface listedness evidence", "Route cases for safety review"],
    neverDoes: ["Make final causality decisions", "Submit regulatory reports", "Close a safety case"],
    contractsPassing: 94, operatingProperties: operatingProperties(3),
    tracker: ["pass", "abstain", "pass", "blocked", "pass", "pass"],
    evidenceByArea: [
      { area: "Case intake", complete: 95, gap: 3, contradiction: 1 },
      { area: "Labelledness", complete: 91, gap: 5, contradiction: 1 },
      { area: "Medical review", complete: 88, gap: 6, contradiction: 2 },
    ],
    contractTests: [
      { id: "PV-P-01", name: "Cites case and labelledness evidence", kind: "positive", result: "pass" },
      { id: "PV-P-02", name: "Routes serious cases for review", kind: "positive", result: "pass" },
      { id: "PV-X-01", name: "Cannot make final PV decision", kind: "prohibited", result: "blocked" },
    ],
    sampleOutput: {
      cited: ["ICSR case NC-PV-4412", "CCDS version 7.2"],
      contradictions: ["Onset date conflicts between narrative and structured field"],
      gaps: ["Reporter follow-up is outstanding"],
      humanReviews: ["Safety physician must confirm seriousness and expectedness"],
    },
    funnelStages: [
      { name: "Received", count: 486 },
      { name: "Deduplicated", count: 441 },
      { name: "Normalized", count: 402 },
      { name: "Clock reconstructed", count: 318 },
      { name: "Routed to human review", count: 96 },
    ],
  }),
  workflow({
    id: "supply", name: "Supply Risk Assessment",
    supports: ["Consolidate supplier evidence", "Identify supply-risk dependencies", "Escalate constrained-material risks"],
    neverDoes: ["Reserve inventory", "Allocate or ship stock", "Approve supplier release"],
    contractsPassing: 95, operatingProperties: operatingProperties(5),
    tracker: ["pass", "pass", "pass", "abstain", "blocked", "pass"],
    evidenceByArea: [
      { area: "Supplier qualification", complete: 94, gap: 3, contradiction: 1 },
      { area: "Inventory evidence", complete: 92, gap: 4, contradiction: 0 },
      { area: "Cold chain", complete: 90, gap: 5, contradiction: 1 },
    ],
    contractTests: [
      { id: "SUP-P-01", name: "Cites approved supplier evidence", kind: "positive", result: "pass" },
      { id: "SUP-P-02", name: "Escalates material constraints", kind: "positive", result: "pass" },
      { id: "SUP-X-01", name: "Cannot reserve or ship stock", kind: "prohibited", result: "blocked" },
    ],
    sampleOutput: {
      cited: ["Approved supplier list ASL-12", "Temperature excursion record TE-884"],
      contradictions: ["Carrier scan sequence contains an out-of-order event"],
      gaps: ["Updated lane qualification is awaiting signature"],
      humanReviews: ["Supply quality lead must approve risk response"],
    },
  }),
];
