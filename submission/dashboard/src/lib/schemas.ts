import { z } from "zod";

export const productIdSchema = z.enum(["all", "NCX-101", "NCB-204", "NCS-310", "NCR-415"]);
export const productSchema = z.object({
  id: productIdSchema,
  name: z.string().min(1),
  description: z.string().min(1),
});
export const decisionStateSchema = z.enum(["Go", "Conditional-Go", "Pivot", "Pause", "Stop"]);
export const injectDimensionSchema = z.enum([
  "Portfolio & strategy",
  "Discovery & model risk",
  "Clinical & trial integrity",
  "GMP & batch release",
  "Quality & data integrity",
  "Pharmacovigilance",
  "Regulatory & submissions",
  "Supply chain & serialization",
  "Privacy & cross-border",
  "Cybersecurity & agentic security",
  "Human factors & responsible AI",
  "Economics & token efficiency",
  "Reliability & continuity",
]);
export const severitySchema = z.enum(["low", "medium", "high", "critical"]);
export const injectStatusSchema = z.enum(["open", "mitigated", "accepted"]);
export const injectProductSchema = z.enum(["All", "NCX-101", "NCB-204", "NCS-310", "NCR-415"]);
export const injectSchema = z.object({
  id: z.string().regex(/^INJ-(0(?:0[1-9]|[1-7][0-9])|08[0-4])$/),
  title: z.string().min(1),
  dimension: injectDimensionSchema,
  severity: severitySchema,
  status: injectStatusSchema,
  product: injectProductSchema,
  evidencePath: z.string().regex(/^(data|knowledge)\/.+\.(csv|md)$/),
  description: z.string().min(1),
  mitigation: z.string().min(1),
});
export const operatingPropertySchema = z.object({
  key: z.string().min(1),
  label: z.string().min(1),
  score: z.number().int().min(0).max(100),
});
export const workflowIdSchema = z.enum(["batch", "pv", "supply"]);
export const workflowSchema = z.object({
  id: workflowIdSchema,
  name: z.string().min(1),
  supports: z.array(z.string().min(1)).min(1),
  neverDoes: z.array(z.string().min(1)).min(1),
  contractsPassing: z.number().int().min(0).max(100),
  operatingProperties: z.array(operatingPropertySchema).length(14),
  tracker: z.array(z.enum(["pass", "abstain", "blocked"])).min(1),
  evidenceByArea: z.array(z.object({
    area: z.string().min(1), complete: z.number().int().min(0).max(100),
    gap: z.number().int().min(0), contradiction: z.number().int().min(0),
  })).min(1),
  contractTests: z.array(z.object({
    id: z.string().min(1), name: z.string().min(1), kind: z.enum(["positive", "prohibited"]),
    result: z.enum(["pass", "blocked"]),
  })).min(1),
  sampleOutput: z.object({
    cited: z.array(z.string()), contradictions: z.array(z.string()),
    gaps: z.array(z.string()), humanReviews: z.array(z.string()),
  }),
  funnelStages: z.array(z.object({ name: z.string().min(1), count: z.number().int().min(0) })).optional(),
});
export const kpiPointSchema = z.object({
  date: z.iso.date(), leadTimeDays: z.number().nonnegative(), evidenceCompleteness: z.number().min(0).max(100),
  openContradictions: z.number().int().nonnegative(), reviewerHoursSaved: z.number().nonnegative(),
  tokenCostUsd: z.number().nonnegative(), inferenceCostUsd: z.number().nonnegative(),
});
export const evidenceGapSchema = z.object({ name: z.string(), impact: z.string(), value: z.string() });
export const costPointSchema = z.object({ category: z.string(), amount: z.number().nonnegative() });
export const hardGateSchema = z.object({ id: z.string(), label: z.string(), pass: z.boolean(), detail: z.string() });
export const continuityMetricSchema = z.object({ label: z.string(), score: z.number().int().min(0).max(100) });
export const heatCellSchema = z.object({ dimension: injectDimensionSchema, severity: severitySchema, count: z.number().int().nonnegative() });
export const dashboardSnapshotSchema = z.object({
  decisionState: decisionStateSchema, decisionRationale: z.string(), requestedDecision: z.string(),
  kpis: z.array(z.object({
    label: z.string(), value: z.string(), delta: z.string(), favorable: z.boolean(), spark: z.array(z.number()),
  })),
  auditReadiness: z.number().int().min(0).max(100), topGaps: z.array(evidenceGapSchema),
  executiveSummary: z.string(),
});

export type ProductId = z.infer<typeof productIdSchema>;
export type Product = z.infer<typeof productSchema>;
export type DecisionState = z.infer<typeof decisionStateSchema>;
export type InjectDimension = z.infer<typeof injectDimensionSchema>;
export type Severity = z.infer<typeof severitySchema>;
export type InjectStatus = z.infer<typeof injectStatusSchema>;
export type Inject = z.infer<typeof injectSchema>;
export type OperatingProperty = z.infer<typeof operatingPropertySchema>;
export type WorkflowId = z.infer<typeof workflowIdSchema>;
export type Workflow = z.infer<typeof workflowSchema>;
export type KpiPoint = z.infer<typeof kpiPointSchema>;
export type EvidenceGap = z.infer<typeof evidenceGapSchema>;
export type CostPoint = z.infer<typeof costPointSchema>;
export type HardGate = z.infer<typeof hardGateSchema>;
export type ContinuityMetric = z.infer<typeof continuityMetricSchema>;
export type HeatCell = z.infer<typeof heatCellSchema>;
export type DashboardSnapshot = z.infer<typeof dashboardSnapshotSchema>;
export type TimeRange = "30d" | "90d" | "12m";
