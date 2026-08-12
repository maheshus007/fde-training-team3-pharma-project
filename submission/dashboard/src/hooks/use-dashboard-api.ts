"use client";
import { useEffect, useState } from "react"; import { toast } from "sonner";
import type { ProductId, TimeRange } from "@/lib/schemas";

export function useDashboardApi<T>(path: string, product: ProductId, timeRange: TimeRange) {
  const [data, setData] = useState<T | null>(null); const [loading, setLoading] = useState(true);
  useEffect(() => { const abort = new AbortController(); setLoading(true); fetch(`${path}?product=${product}&timeRange=${timeRange}`, { signal: abort.signal }).then(async r => { if (!r.ok) throw new Error("Dashboard data unavailable"); return r.json() as Promise<T>; }).then(setData).catch(e => { if (e.name !== "AbortError") toast.error("Could not load dashboard data"); }).finally(() => setLoading(false)); return () => abort.abort(); }, [path, product, timeRange]);
  return { data, loading };
}
