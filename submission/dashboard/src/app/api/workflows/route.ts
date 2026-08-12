import { USE_MOCK } from "@/lib/config";
import { workflows } from "@/lib/data";
import { productIdSchema } from "@/lib/schemas";
import { type NextRequest, NextResponse } from "next/server";

export function GET(request: NextRequest) {
  if (!USE_MOCK) return NextResponse.json({ error: "Mock data is disabled." }, { status: 503 });
  const product = productIdSchema.safeParse(request.nextUrl.searchParams.get("product") ?? "all");
  if (!product.success) return NextResponse.json({ error: "Invalid product." }, { status: 400 });
  return NextResponse.json({ product: product.data, workflows });
}
