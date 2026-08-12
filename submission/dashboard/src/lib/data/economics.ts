import type { CostPoint } from "@/lib/schemas";

export const costBreakdown: CostPoint[] = [
  { category: "Model inference", amount: 5_480 },
  { category: "Evidence retrieval", amount: 2_160 },
  { category: "Human review", amount: 8_940 },
  { category: "Platform controls", amount: 3_620 },
  { category: "Validation & assurance", amount: 4_180 },
];

export const economicsKpis = {
  costPerTaskUsd: 18.42,
  costAvoidanceUsd: 42_600,
  reviewerHoursSaved: 1_986,
  tasksCompleted: 1_324,
  budgetVariancePercent: -7.8,
  humanReviewSharePercent: 36,
};
