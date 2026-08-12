import {
  injectDimensionSchema,
  injectSchema,
  type Inject,
  type InjectDimension,
  type ProductId,
  type Severity,
} from "@/lib/schemas";
import { mulberry32 } from "@/lib/seed";

const dimensions = injectDimensionSchema.options;

const titles: Record<InjectDimension, string[]> = {
  "Portfolio & strategy": [
    "Patent-cliff pressure on NCX-101 release cadence",
    "Portfolio prioritisation conflicts with Quality capacity",
    "Compassionate-use demand outpaces NCS-310 evidence pack",
  ],
  "Discovery & model risk": [
    "Unverified model card for extraction workload",
    "Fallback small model loses non-English fidelity",
    "Training corpus includes unapproved affiliate notes",
  ],
  "Clinical & trial integrity": [
    "Site protocol version lags global current",
    "IRT vs EDC visit window mismatch",
    "Eligibility context unresolved for S-301 cohort",
  ],
  "GMP & batch release": [
    "Genealogy branch missing for consumed lot",
    "EM excursion conflicts with batch disposition draft",
    "CMO audit package incomplete for release review",
  ],
  "Quality & data integrity": [
    "Conflicting assay units across LIMS exports",
    "Deviation CAPA linkage broken in QMS extract",
    "Spreadsheet override lacks ALCOA+ provenance",
  ],
  "Pharmacovigilance": [
    "Duplicate ICSR cluster across affiliates",
    "Listedness evidence conflicts for same PT",
    "Reporting clock reconstruction incomplete",
  ],
  "Regulatory & submissions": [
    "RIM authority date stale vs dossier cite",
    "Labeling variation not reflected in local pack",
    "Submission artefact hash mismatch",
  ],
  "Supply chain & serialization": [
    "Cold-chain gap on lane qualification",
    "Serialization event missing for hospital shipment",
    "CMO capacity draft risks silent allocation",
  ],
  "Privacy & cross-border": [
    "DSR deletion blocked by legal hold",
    "Cross-affiliate purpose limitation breach attempt",
    "Pseudonym key exposed in narrative extract",
  ],
  "Cybersecurity & agentic security": [
    "Prompt injection in supplier deviation PDF",
    "Poisoned tool manifest requests write access",
    "Contractor IAM revocation lag in gateway cache",
  ],
  "Human factors & responsible AI": [
    "Automation bias on omitted critical deviation",
    "Colour-only warning fails accessibility check",
    "Language inequity for Arabic/Hindi narratives",
  ],
  "Economics & token efficiency": [
    "Denial-of-wallet oversized document flood",
    "Model price shock on preferred vendor",
    "Hidden human-review cost omitted from business case",
  ],
  "Reliability & continuity": [
    "Primary AI region outage during batch review",
    "AI-disabled continuity for 14 days required",
    "Checkpoint age exceeds resume policy",
  ],
};

const products = ["All", "NCX-101", "NCB-204", "NCS-310", "NCR-415"] as const;
const severityPlan: Severity[] = [
  ...Array<Severity>(13).fill("critical"),
  ...Array<Severity>(21).fill("high"),
  ...Array<Severity>(29).fill("medium"),
  ...Array<Severity>(21).fill("low"),
];

const random = mulberry32(42);

function pad(value: number): string {
  return value.toString().padStart(3, "0");
}

export const injects: Inject[] = Array.from({ length: 84 }, (_, index) => {
  const dimension = dimensions[index % dimensions.length];
  const severity = severityPlan[(index * 17) % severityPlan.length];
  const titlePool = titles[dimension];
  const title = titlePool[Math.floor(random() * titlePool.length)];
  const status = index % 7 === 0 ? "accepted" : index % 3 === 0 ? "open" : "mitigated";
  const product = products[(index * 3 + Math.floor(random() * products.length)) % products.length];
  const slug = dimension.toLowerCase().replaceAll(/[^a-z0-9]+/g, "-");
  const evidencePath =
    index % 2 === 0
      ? `data/${slug}-evidence-${pad(index + 1)}.csv`
      : `knowledge/${slug}-control-${pad(index + 1)}.md`;

  return injectSchema.parse({
    id: `INJ-${pad(index + 1)}`,
    title,
    dimension,
    severity,
    status,
    product,
    evidencePath,
    description: `${title}. Challenge inject for ${dimension} affecting ${product === "All" ? "the NovaCura portfolio" : product}. AI may only surface evidence, contradictions, gaps and abstentions — humans retain regulated decisions.`,
    mitigation:
      status === "mitigated"
        ? "Control owner recorded corrective evidence; retain for periodic effectiveness review."
        : status === "accepted"
          ? "Risk acceptance is documented with accountable owner and next review date."
          : "Hold the affected workflow step, collect authoritative evidence, and obtain human approval before resumption.",
  });
});

export function filterInjects(product: ProductId, dimension?: InjectDimension): Inject[] {
  return injects.filter(
    (inject) =>
      (product === "all" || inject.product === "All" || inject.product === product) &&
      (dimension === undefined || inject.dimension === dimension),
  );
}
