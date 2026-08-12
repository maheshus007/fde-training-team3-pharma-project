import { USE_MOCK } from "@/lib/config";
import { filterInjects } from "@/lib/data";
import { injectDimensionSchema, productIdSchema } from "@/lib/schemas";
import { type NextRequest, NextResponse } from "next/server";

export function GET(request: NextRequest) {
  if (!USE_MOCK) return NextResponse.json({ error: "Mock data is disabled." }, { status: 503 });
  const product = productIdSchema.safeParse(request.nextUrl.searchParams.get("product") ?? "all");
  const dimension = injectDimensionSchema.safeParse(request.nextUrl.searchParams.get("dimension"));
  if (!product.success) return NextResponse.json({ error: "Invalid product." }, { status: 400 });
  if (request.nextUrl.searchParams.has("dimension") && !dimension.success) {
    return NextResponse.json({ error: "Invalid dimension." }, { status: 400 });
  }
  return NextResponse.json({ injects: filterInjects(product.data, dimension.success ? dimension.data : undefined) });
}
