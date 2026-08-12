import { injectDimensionSchema, type InjectDimension, type InjectStatus, type Severity } from "@/lib/schemas";

export const CHART_COLORS = ["#00A896", "#0A1F3C", "#E8A33D", "#1C3A5E", "#02C39A", "#E86A5B"] as const;

export const SEMANTIC_COLORS = {
  teal: "#00A896",
  navy: "#0A1F3C",
  amber: "#E8A33D",
  slate: "#1C3A5E",
  emerald: "#02C39A",
  danger: "#E86A5B",
} as const;

export const chartConfig = {
  evidenceCompleteness: { label: "Evidence completeness", color: SEMANTIC_COLORS.teal },
  leadTimeDays: { label: "Lead time", color: SEMANTIC_COLORS.navy },
  openContradictions: { label: "Open contradictions", color: SEMANTIC_COLORS.danger },
  reviewerHoursSaved: { label: "Reviewer hours saved", color: SEMANTIC_COLORS.emerald },
  cost: { label: "Cost", color: SEMANTIC_COLORS.amber },
} satisfies Record<string, { label: string; color: string }>;

/**
 * Extended palette so each of the 13 challenge dimensions keeps a stable,
 * distinguishable colour across the donut, heatmap, and legends.
 */
const DIMENSION_PALETTE = [
  "#00A896",
  "#0A1F3C",
  "#E8A33D",
  "#1C3A5E",
  "#02C39A",
  "#E86A5B",
  "#5E91C4",
  "#8B5CF6",
  "#D4A373",
  "#4C956C",
  "#B76935",
  "#6D6875",
  "#457B9D",
] as const;

export const DIMENSION_COLORS: Record<InjectDimension, string> = Object.fromEntries(
  injectDimensionSchema.options.map((dimension, index) => [dimension, DIMENSION_PALETTE[index % DIMENSION_PALETTE.length]]),
) as Record<InjectDimension, string>;

export const SEVERITY_COLORS: Record<Severity, string> = {
  critical: "#C0392B",
  high: SEMANTIC_COLORS.amber,
  medium: "#5E91C4",
  low: SEMANTIC_COLORS.emerald,
};

export const STATUS_COLORS: Record<InjectStatus, string> = {
  open: SEMANTIC_COLORS.danger,
  mitigated: SEMANTIC_COLORS.teal,
  accepted: SEMANTIC_COLORS.slate,
};
