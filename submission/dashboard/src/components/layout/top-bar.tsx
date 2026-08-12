"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useFilters } from "@/components/providers/filter-provider";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import type { ProductId, TimeRange } from "@/lib/schemas";

const products: { id: ProductId; label: string }[] = [
  { id: "all", label: "All products" },
  { id: "NCX-101", label: "NCX-101" },
  { id: "NCB-204", label: "NCB-204" },
  { id: "NCS-310", label: "NCS-310" },
  { id: "NCR-415", label: "NCR-415" },
];

const ranges: { id: TimeRange; label: string }[] = [
  { id: "30d", label: "30d" },
  { id: "90d", label: "90d" },
  { id: "12m", label: "12m" },
];

export function TopBar() {
  const { product, timeRange, setProduct, setTimeRange } = useFilters();
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex flex-wrap items-center gap-3 border-b bg-background/90 px-4 py-3 backdrop-blur md:px-6">
      <SidebarTrigger className="md:hidden" />
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium">Decision intelligence within defined boundaries</p>
      </div>
      <span className="rounded-full border border-emerald-300 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800 dark:border-emerald-800 dark:bg-emerald-950 dark:text-emerald-200">
        AI supports · humans decide
      </span>
      <select
        aria-label="Product filter"
        className="h-9 rounded-md border bg-background px-3 text-sm"
        value={product}
        onChange={(event) => setProduct(event.target.value as ProductId)}
      >
        {products.map((item) => (
          <option key={item.id} value={item.id}>
            {item.label}
          </option>
        ))}
      </select>
      <select
        aria-label="Time range filter"
        className="h-9 rounded-md border bg-background px-3 text-sm"
        value={timeRange}
        onChange={(event) => setTimeRange(event.target.value as TimeRange)}
      >
        {ranges.map((item) => (
          <option key={item.id} value={item.id}>
            {item.label}
          </option>
        ))}
      </select>
      <Button
        variant="outline"
        size="icon"
        aria-label="Toggle theme"
        onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      >
        <Sun className="size-4 dark:hidden" />
        <Moon className="hidden size-4 dark:block" />
      </Button>
    </header>
  );
}
