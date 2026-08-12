import { kpiPointSchema, type KpiPoint, type ProductId, type TimeRange } from "@/lib/schemas";
import { mulberry32 } from "@/lib/seed";

const random = mulberry32(42);
const productBias: Record<ProductId, number> = { all: 0, "NCX-101": 1, "NCB-204": -1, "NCS-310": 2, "NCR-415": -2 };

export const kpiSeries: KpiPoint[] = Array.from({ length: 12 }, (_, index) => {
  const month = index + 1;
  return kpiPointSchema.parse({
    date: `2026-${month.toString().padStart(2, "0")}-01`,
    leadTimeDays: Number((8.8 - index * 0.22 + random() * 0.3).toFixed(1)),
    evidenceCompleteness: Math.min(99, 82 + index + Math.floor(random() * 3)),
    openContradictions: Math.max(3, 19 - index - Math.floor(random() * 3)),
    reviewerHoursSaved: 118 + index * 11 + Math.floor(random() * 8),
    tokenCostUsd: 820 + index * 42 + Math.floor(random() * 60),
    inferenceCostUsd: 370 + index * 28 + Math.floor(random() * 35),
  });
});

export function getKpis(timeRange: TimeRange, product: ProductId = "all"): KpiPoint[] {
  const count = timeRange === "30d" ? 1 : timeRange === "90d" ? 3 : 12;
  const bias = productBias[product];
  return kpiSeries.slice(-count).map((point) => ({
    ...point,
    leadTimeDays: Number(Math.max(1, point.leadTimeDays - bias * 0.08).toFixed(1)),
    evidenceCompleteness: Math.min(100, Math.max(0, point.evidenceCompleteness + bias)),
    openContradictions: Math.max(0, point.openContradictions - bias),
    reviewerHoursSaved: Math.max(0, point.reviewerHoursSaved + bias * 4),
  }));
}
