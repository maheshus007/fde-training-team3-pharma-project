import { USE_MOCK } from "@/lib/config";
import { costBreakdown, economicsKpis } from "@/lib/data";
import { productIdSchema, type TimeRange } from "@/lib/schemas";
import { type NextRequest, NextResponse } from "next/server";

const timeRanges = new Set<TimeRange>(["30d", "90d", "12m"]);

export function GET(request: NextRequest) {
  if (!USE_MOCK) return NextResponse.json({ error: "Mock data is disabled." }, { status: 503 });
  const product = productIdSchema.safeParse(request.nextUrl.searchParams.get("product") ?? "all");
  const timeRange = request.nextUrl.searchParams.get("timeRange") ?? "12m";
  if (!product.success || !timeRanges.has(timeRange as TimeRange)) {
    return NextResponse.json({ error: "Invalid product or timeRange." }, { status: 400 });
  }
  return NextResponse.json({ product: product.data, timeRange, costBreakdown, ...economicsKpis });
}
