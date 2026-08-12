"use client";

import dynamic from "next/dynamic";
import { useMemo } from "react";

import { SrOnlyTable } from "@/components/charts/sr-only-table";
import { SEMANTIC_COLORS } from "@/lib/chart-theme";
import { injectDimensionSchema, severitySchema, type HeatCell } from "@/lib/schemas";

/**
 * ApexCharts renders to canvas/SVG using browser globals, so it must never
 * run during server-side rendering.
 */
const ApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

const DIMENSIONS = injectDimensionSchema.options;
const SEVERITIES = severitySchema.options;

export function RiskHeatmap({ data, height = 380 }: { data: HeatCell[]; height?: number }) {
  const series = useMemo(
    () =>
      DIMENSIONS.map((dimension) => ({
        name: dimension,
        data: SEVERITIES.map((severity) => {
          const cell = data.find((item) => item.dimension === dimension && item.severity === severity);
          return { x: severity, y: cell?.count ?? 0 };
        }),
      })),
    [data],
  );

  const options = {
    chart: { type: "heatmap" as const, toolbar: { show: false }, fontFamily: "inherit", background: "transparent" },
    dataLabels: { enabled: true, style: { colors: ["#0A1F3C"] } },
    legend: { position: "bottom" as const, fontSize: "12px" },
    xaxis: { position: "top" as const, labels: { style: { fontSize: "11px" } } },
    yaxis: { labels: { style: { fontSize: "11px" } } },
    grid: { padding: { left: 8, right: 8 } },
    plotOptions: {
      heatmap: {
        radius: 4,
        colorScale: {
          ranges: [
            { from: 0, to: 0, color: "#E4EAF0", name: "None" },
            { from: 1, to: 2, color: SEMANTIC_COLORS.emerald, name: "Low" },
            { from: 3, to: 5, color: SEMANTIC_COLORS.amber, name: "Elevated" },
            { from: 6, to: 999, color: SEMANTIC_COLORS.danger, name: "Concentrated" },
          ],
        },
      },
    },
    tooltip: {
      y: {
        formatter: (value: number) => `${value} injects`,
      },
    },
  };

  return (
    <div>
      <ApexChart type="heatmap" height={height} options={options} series={series} />
      <SrOnlyTable
        caption="Inject count by challenge dimension and severity"
        headers={["Dimension", "Severity", "Count"]}
        rows={data.map((cell) => [cell.dimension, cell.severity, cell.count])}
      />
    </div>
  );
}
