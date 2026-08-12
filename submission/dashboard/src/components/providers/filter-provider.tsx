"use client";

import { createContext, useContext } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import type { ProductId, TimeRange } from "@/lib/schemas";

type Filters = { product: ProductId; timeRange: TimeRange; setProduct: (value: ProductId) => void; setTimeRange: (value: TimeRange) => void };
const FilterContext = createContext<Filters | null>(null);
const products = ["all", "NCX-101", "NCB-204", "NCS-310", "NCR-415"] as const;
const ranges = ["30d", "90d", "12m"] as const;

export function FilterProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter(); const pathname = usePathname(); const params = useSearchParams();
  const product = products.includes(params.get("product") as ProductId) ? params.get("product") as ProductId : "all";
  const timeRange = ranges.includes(params.get("timeRange") as TimeRange) ? params.get("timeRange") as TimeRange : "12m";
  const set = (key: "product" | "timeRange", value: string) => {
    const next = new URLSearchParams(params.toString()); next.set(key, value);
    router.replace(`${pathname}?${next.toString()}`, { scroll: false });
  };
  const value = { product, timeRange, setProduct: (v: ProductId) => set("product", v), setTimeRange: (v: TimeRange) => set("timeRange", v) };
  return <FilterContext.Provider value={value}>{children}</FilterContext.Provider>;
}
export function useFilters() { const value = useContext(FilterContext); if (!value) throw new Error("useFilters must be used inside FilterProvider"); return value; }
