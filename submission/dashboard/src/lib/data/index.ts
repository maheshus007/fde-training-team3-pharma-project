import { costBreakdown, economicsKpis } from "@/lib/data/economics";
import { hardGates, continuityMetrics, boundaryDoes, boundaryNever } from "@/lib/data/governance";
import { filterInjects, injects } from "@/lib/data/injects";
import { getKpis } from "@/lib/data/kpis";
import { products } from "@/lib/data/products";
import { workflows } from "@/lib/data/workflows";
import { delta } from "@/lib/format";
import {
  type DashboardSnapshot, type HeatCell, type Inject, type InjectDimension, type ProductId, type TimeRange,
} from "@/lib/schemas";

export function buildHeatmap(items: Inject[]): HeatCell[] {
  const severities = ["low", "medium", "high", "critical"] as const;
  const dimensions = [...new Set(items.map((item) => item.dimension))] as InjectDimension[];
  return dimensions.flatMap((dimension) => severities.map((severity) => ({
    dimension, severity, count: items.filter((item) => item.dimension === dimension && item.severity === severity).length,
  })));
}

export const injectsByDimension = Object.fromEntries(
  [...new Set(injects.map((inject) => inject.dimension))].map((dimension) => [
    dimension,
    injects.filter((inject) => inject.dimension === dimension),
  ]),
) as Record<InjectDimension, Inject[]>;

/**
 * A CFO-readable narrative covering the problem, the three supported
 * workflows, the current governance posture, the safety boundary, and the
 * decision being requested of leadership.
 */
const EXECUTIVE_SUMMARY = [
  "NovaCura's batch release, pharmacovigilance, and supply-risk teams spend the majority of reviewer hours re-assembling evidence that already exists across LIMS, QMS, and safety systems, which slows release lead-time and obscures where governance attention is needed.",
  "AEGIS-PHARMA assembles cited, reviewer-ready evidence for Batch Evidence Triage, PV Case Prioritisation, and Supply Risk Assessment, flags contradictions and gaps instead of resolving them, and routes every disposition, causality, and allocation decision to an accountable human.",
  "The portfolio's current posture is Conditional-Go: evidence completeness and audit readiness are strong, while contradiction closure and reviewer capacity remain active management conditions rather than blocking risks.",
  "A hard safety boundary is enforced end-to-end \u2014 the system cannot disposition a batch, close a PV case, or reserve and ship inventory \u2014 so gains in speed and cost never come at the expense of regulated authority.",
  "We are asking leadership to approve a controlled expansion with monthly quality and safety governance review, keeping all three supported workflows within their bounded evidence-and-routing role.",
].join(" ");

function buildSnapshot(product: ProductId, timeRange: TimeRange): DashboardSnapshot {
  const kpis = getKpis(timeRange, product);
  const latest = kpis.at(-1);
  if (latest === undefined) {
    throw new Error("KPI series must contain at least one point.");
  }
  const prior = kpis.at(-2) ?? latest;
  const productLabel = products.find((item) => item.id === product)?.name ?? "NovaCura portfolio";

  const leadTimeDelta = Number((latest.leadTimeDays - prior.leadTimeDays).toFixed(1));
  const evidenceDelta = latest.evidenceCompleteness - prior.evidenceCompleteness;
  const contradictionsDelta = latest.openContradictions - prior.openContradictions;
  const reviewerHoursDelta = latest.reviewerHoursSaved - prior.reviewerHoursSaved;

  return {
    decisionState: "Conditional-Go",
    decisionRationale: `${productLabel} has strong evidence control coverage, while contradiction closure and human-review capacity remain active management conditions.`,
    requestedDecision: "Approve a controlled expansion with monthly quality and safety governance review.",
    kpis: [
      {
        label: "Release lead-time (days)",
        value: `${latest.leadTimeDays.toFixed(1)} days`,
        delta: delta(leadTimeDelta, " days"),
        favorable: leadTimeDelta <= 0,
        spark: kpis.map((item) => item.leadTimeDays),
      },
      {
        label: "Evidence completeness",
        value: `${latest.evidenceCompleteness}%`,
        delta: delta(evidenceDelta, " pts"),
        favorable: evidenceDelta >= 0,
        spark: kpis.map((item) => item.evidenceCompleteness),
      },
      {
        label: "Open contradictions",
        value: String(latest.openContradictions),
        delta: delta(contradictionsDelta),
        favorable: contradictionsDelta <= 0,
        spark: kpis.map((item) => item.openContradictions),
      },
      {
        label: "Reviewer hours saved / week",
        value: `${latest.reviewerHoursSaved} hrs`,
        delta: delta(reviewerHoursDelta, " hrs"),
        favorable: reviewerHoursDelta >= 0,
        spark: kpis.map((item) => item.reviewerHoursSaved),
      },
    ],
    auditReadiness: 94,
    topGaps: [
      { name: "Deviation closure evidence", impact: "High", value: "5 records awaiting signed closure" },
      { name: "PV reporter follow-up", impact: "Medium", value: "6 cases awaiting confirmation" },
      { name: "Lane qualification update", impact: "Medium", value: "3 supplier lanes pending signature" },
      { name: "CMO audit packet completeness", impact: "High", value: "2 packs missing contemporaneous evidence" },
      { name: "Cold-chain sensor continuity", impact: "Medium", value: "1 lane with gap in excursion log" },
    ],
    executiveSummary: EXECUTIVE_SUMMARY,
  };
}

export function getDashboardData({ product = "all", timeRange = "12m" }: { product?: ProductId; timeRange?: TimeRange } = {}) {
  const filteredInjects = filterInjects(product);
  return {
    products, selectedProduct: product, selectedTimeRange: timeRange,
    snapshot: buildSnapshot(product, timeRange),
    injects: filteredInjects, heatmap: buildHeatmap(filteredInjects),
    workflows, kpis: getKpis(timeRange, product),
    governance: { hardGates, continuityMetrics, boundaryDoes, boundaryNever },
    economics: { costBreakdown, ...economicsKpis },
  };
}

export { injects, filterInjects, workflows, products, hardGates, continuityMetrics, boundaryDoes, boundaryNever, costBreakdown, economicsKpis, getKpis };
