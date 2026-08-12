"use client";

import { useMemo, useState } from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type PaginationState,
  type SortingState,
} from "@tanstack/react-table";
import { ArrowDown, ArrowUp, ArrowUpDown, Download } from "lucide-react";

import { SeverityBadge, StatusBadge } from "@/components/badges/inject-badges";
import { ChartCard } from "@/components/cards/chart-card";
import { Donut, InjectStatusBar } from "@/components/charts/dashboard-charts";
import { RiskHeatmap } from "@/components/charts/risk-heatmap";
import { FadeIn } from "@/components/motion/fade-in";
import { useFilters } from "@/components/providers/filter-provider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { getDashboardData } from "@/lib/data";
import { cn } from "@/lib/utils";
import { injectDimensionSchema, injectStatusSchema, severitySchema, type Inject } from "@/lib/schemas";

const columnHelper = createColumnHelper<Inject>();

const columns = [
  columnHelper.accessor("id", {
    header: "ID",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("title", { header: "Challenge" }),
  columnHelper.accessor("dimension", { header: "Dimension" }),
  columnHelper.accessor("severity", {
    header: "Severity",
    cell: (info) => <SeverityBadge severity={info.getValue()} />,
  }),
  columnHelper.accessor("status", {
    header: "Status",
    cell: (info) => <StatusBadge status={info.getValue()} />,
  }),
  columnHelper.accessor("product", { header: "Product" }),
  columnHelper.accessor("evidencePath", {
    header: "Evidence",
    cell: (info) => <span className="font-mono text-xs text-muted-foreground">{info.getValue()}</span>,
  }),
];

const DIMENSIONS = injectDimensionSchema.options;
const SEVERITIES = severitySchema.options;
const STATUSES = injectStatusSchema.options;
const PAGE_SIZE = 10;

function downloadInjectsCsv(rows: Inject[]) {
  const header = ["ID", "Title", "Dimension", "Severity", "Status", "Product", "Evidence Path"];
  const escape = (value: string) => `"${value.replaceAll('"', '""')}"`;
  const lines = rows.map((row) =>
    [row.id, row.title, row.dimension, row.severity, row.status, row.product, row.evidencePath].map(escape).join(","),
  );
  const csv = [header.join(","), ...lines].join("\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "aegis-injects.csv";
  link.click();
  URL.revokeObjectURL(url);
}

export default function RiskPage() {
  const data = getDashboardData(useFilters());
  const [query, setQuery] = useState("");
  const [dimension, setDimension] = useState<string>("all");
  const [severity, setSeverity] = useState<string>("all");
  const [status, setStatus] = useState<string>("all");
  const [sorting, setSorting] = useState<SortingState>([]);
  const [pagination, setPagination] = useState<PaginationState>({ pageIndex: 0, pageSize: PAGE_SIZE });
  const [selected, setSelected] = useState<Inject | null>(null);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return data.injects.filter((inject) => {
      if (dimension !== "all" && inject.dimension !== dimension) return false;
      if (severity !== "all" && inject.severity !== severity) return false;
      if (status !== "all" && inject.status !== status) return false;
      if (!needle) return true;
      return `${inject.id} ${inject.title} ${inject.dimension}`.toLowerCase().includes(needle);
    });
  }, [data.injects, query, dimension, severity, status]);

  const table = useReactTable({
    data: filtered,
    columns,
    state: { sorting, pagination },
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  const hasActiveFilters = query !== "" || dimension !== "all" || severity !== "all" || status !== "all";

  function clearFilters() {
    setQuery("");
    setDimension("all");
    setSeverity("all");
    setStatus("all");
  }

  return (
    <div className="space-y-6">
      <FadeIn>
        <div>
          <h1 className="text-3xl font-semibold">Evidence &amp; risk</h1>
          <p className="mt-2 text-muted-foreground">
            All 84 resilience-test injects across the 13 challenge dimensions.             Filtering here never changes an
            inject&rsquo;s recorded outcome &mdash; it only changes what you are viewing.
          </p>
        </div>
      </FadeIn>

      <FadeIn delay={0.05}>
        <section className="grid gap-4 lg:grid-cols-2">
          <ChartCard
            title="Inject risk heatmap"
            why="Coverage across challenge dimensions and severities prevents blind spots in resilience testing."
          >
            <RiskHeatmap data={data.heatmap} />
          </ChartCard>
          <ChartCard
            title="Inject dimensions"
            why="Dimension distribution shows where resilience work is concentrated. Click a segment to filter the table below."
          >
            <Donut injects={data.injects} onSelectDimension={setDimension} />
          </ChartCard>
        </section>
      </FadeIn>

      <FadeIn delay={0.1}>
        <ChartCard
          title="Severity vs status"
          why="Cross-referencing severity with disposition status shows whether the highest-risk injects are actually resolved."
        >
          <InjectStatusBar injects={filtered} />
        </ChartCard>
      </FadeIn>

      <FadeIn delay={0.15}>
        <section className="rounded-2xl border bg-card p-5">
          <div className="flex flex-wrap items-center gap-3">
            <Input
              className="max-w-xs"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search 84 injects by ID, title, dimension"
              aria-label="Search injects"
            />
            <Select value={dimension} onValueChange={setDimension}>
              <SelectTrigger className="w-56"><SelectValue placeholder="Dimension" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All dimensions</SelectItem>
                {DIMENSIONS.map((item) => (
                  <SelectItem key={item} value={item}>{item}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={severity} onValueChange={setSeverity}>
              <SelectTrigger className="w-36"><SelectValue placeholder="Severity" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All severity</SelectItem>
                {SEVERITIES.map((item) => (
                  <SelectItem key={item} value={item} className="capitalize">{item}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={status} onValueChange={setStatus}>
              <SelectTrigger className="w-36"><SelectValue placeholder="Status" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All status</SelectItem>
                {STATUSES.map((item) => (
                  <SelectItem key={item} value={item} className="capitalize">{item}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            {hasActiveFilters && (
              <Button variant="ghost" size="sm" onClick={clearFilters}>Clear filters</Button>
            )}
            <Button
              variant="outline"
              size="sm"
              className="ml-auto"
              onClick={() => downloadInjectsCsv(filtered)}
            >
              <Download /> Export CSV
            </Button>
          </div>

          <div className="mt-4 overflow-x-auto">
            <Table>
              <TableHeader>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => {
                      const sortDirection = header.column.getIsSorted();
                      return (
                        <TableHead key={header.id}>
                          {header.isPlaceholder ? null : (
                            <button
                              type="button"
                              className={cn(
                                "flex items-center gap-1",
                                header.column.getCanSort() && "cursor-pointer select-none hover:text-foreground",
                              )}
                              onClick={header.column.getToggleSortingHandler()}
                            >
                              {flexRender(header.column.columnDef.header, header.getContext())}
                              {header.column.getCanSort() && (
                                sortDirection === "asc" ? <ArrowUp className="size-3" />
                                : sortDirection === "desc" ? <ArrowDown className="size-3" />
                                : <ArrowUpDown className="size-3 opacity-40" />
                              )}
                            </button>
                          )}
                        </TableHead>
                      );
                    })}
                  </TableRow>
                ))}
              </TableHeader>
              <TableBody>
                {table.getRowModel().rows.map((row) => (
                  <TableRow
                    key={row.id}
                    className="cursor-pointer"
                    onClick={() => setSelected(row.original)}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                    ))}
                  </TableRow>
                ))}
                {table.getRowModel().rows.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={columns.length} className="py-8 text-center text-muted-foreground">
                      No injects match the current filters.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>

          <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-muted-foreground">
            <span>
              Showing {filtered.length === 0 ? 0 : pagination.pageIndex * pagination.pageSize + 1}
              &ndash;{Math.min((pagination.pageIndex + 1) * pagination.pageSize, filtered.length)} of {filtered.length} injects
              {filtered.length !== data.injects.length && ` (filtered from ${data.injects.length})`}
            </span>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
                Previous
              </Button>
              <span>Page {pagination.pageIndex + 1} of {Math.max(1, table.getPageCount())}</span>
              <Button variant="outline" size="sm" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
                Next
              </Button>
            </div>
          </div>
        </section>
      </FadeIn>

      <Sheet open={selected !== null} onOpenChange={(open) => !open && setSelected(null)}>
        <SheetContent>
          {selected && (
            <>
              <SheetHeader>
                <SheetTitle>{selected.id} &middot; {selected.title}</SheetTitle>
                <SheetDescription>{selected.dimension} &middot; {selected.product}</SheetDescription>
              </SheetHeader>
              <div className="space-y-4 overflow-y-auto px-4 pb-4 text-sm">
                <div className="flex flex-wrap gap-2">
                  <SeverityBadge severity={selected.severity} />
                  <StatusBadge status={selected.status} />
                </div>
                <div>
                  <h3 className="font-medium text-foreground">Description</h3>
                  <p className="mt-1 text-muted-foreground">{selected.description}</p>
                </div>
                <div>
                  <h3 className="font-medium text-foreground">Mitigation</h3>
                  <p className="mt-1 text-muted-foreground">{selected.mitigation}</p>
                </div>
                <div>
                  <h3 className="font-medium text-foreground">Evidence path</h3>
                  <p className="mt-1 break-all font-mono text-xs text-muted-foreground">{selected.evidencePath}</p>
                </div>
              </div>
            </>
          )}
        </SheetContent>
      </Sheet>
    </div>
  );
}
