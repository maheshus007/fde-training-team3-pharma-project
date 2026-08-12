"use client";

import type { ApexOptions } from "apexcharts";
import dynamic from "next/dynamic";

import { SrOnlyTable } from "@/components/charts/sr-only-table";
import { SEMANTIC_COLORS } from "@/lib/chart-theme";
import type { Workflow } from "@/lib/schemas";

/**
 * ApexCharts renders to canvas/SVG using browser globals, so it must never
 * run during server-side rendering.
 */
const ApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

const STAGE_COLORS = [SEMANTIC_COLORS.navy, SEMANTIC_COLORS.slate, SEMANTIC_COLORS.teal, SEMANTIC_COLORS.emerald, SEMANTIC_COLORS.amber];

export function PvFunnel({ stages }: { stages: NonNullable<Workflow["funnelStages"]> }) {
  const series = [{ name: "Cases", data: stages.map((stage) => ({ x: stage.name, y: stage.count })) }];

  const options: ApexOptions = {
    chart: { type: "bar", toolbar: { show: false }, fontFamily: "inherit", background: "transparent" },
    plotOptions: { bar: { horizontal: true, isFunnel: true, distributed: true, barHeight: "82%" } },
    colors: STAGE_COLORS,
    dataLabels: { enabled: true, style: { colors: ["#ffffff"], fontSize: "12px" } },
    legend: { show: false },
    xaxis: { categories: stages.map((stage) => stage.name) },
    tooltip: { y: { formatter: (value: number) => `${value.toLocaleString()} cases` } },
  };

  return (
    <div>
      <ApexChart type="bar" height={300} options={options} series={series} />
      <SrOnlyTable
        caption="Pharmacovigilance case funnel by stage"
        headers={["Stage", "Case count"]}
        rows={stages.map((stage) => [stage.name, stage.count])}
      />
    </div>
  );
}
