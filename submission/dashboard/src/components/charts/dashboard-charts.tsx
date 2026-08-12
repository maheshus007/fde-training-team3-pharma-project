"use client";

import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  Pie,
  PieChart,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  RadialBar,
  RadialBarChart,
  ReferenceDot,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { SrOnlyTable } from "@/components/charts/sr-only-table";
import { DIMENSION_COLORS, SEMANTIC_COLORS, STATUS_COLORS } from "@/lib/chart-theme";
import type { CostPoint, Inject, InjectStatus, KpiPoint, Severity, Workflow } from "@/lib/schemas";

const TARGET_LEAD_TIME_DAYS = 7;
const SEVERITY_ORDER: Severity[] = ["critical", "high", "medium", "low"];
const STATUS_ORDER: InjectStatus[] = ["open", "mitigated", "accepted"];
const COST_BREAKDOWN_PALETTE = [
  SEMANTIC_COLORS.teal,
  SEMANTIC_COLORS.navy,
  SEMANTIC_COLORS.amber,
  SEMANTIC_COLORS.slate,
  SEMANTIC_COLORS.emerald,
];

/** Release lead-time trend against the 7-day target line. */
export function LeadTimeArea({ data }: { data: KpiPoint[] }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={210}>
        <AreaChart data={data} margin={{ left: -16, right: 8, top: 8 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" hide />
          <YAxis width={32} tickLine={false} axisLine={false} />
          <Tooltip formatter={(value) => [`${String(value)} days`, "Lead time"]} />
          <Area
            type="monotone"
            dataKey="leadTimeDays"
            name="Lead time"
            stroke={SEMANTIC_COLORS.teal}
            fill={SEMANTIC_COLORS.teal}
            fillOpacity={0.16}
            strokeWidth={2}
          />
          <Line
            dataKey={() => TARGET_LEAD_TIME_DAYS}
            name="Target"
            stroke={SEMANTIC_COLORS.amber}
            strokeDasharray="5 5"
            strokeWidth={2}
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption={`Release lead-time by month against the ${TARGET_LEAD_TIME_DAYS}-day target`}
        headers={["Month", "Lead time (days)"]}
        rows={data.map((point) => [point.date, point.leadTimeDays])}
      />
    </div>
  );
}

/** Circular gauge summarising audit readiness as a single percentage. */
export function AuditRadial({ value }: { value: number }) {
  return (
    <div className="relative h-52 w-full min-w-0">
      <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={180}>
        <RadialBarChart innerRadius="70%" outerRadius="100%" data={[{ value }]} startAngle={90} endAngle={-270}>
          <RadialBar dataKey="value" fill={SEMANTIC_COLORS.teal} background cornerRadius={8} />
        </RadialBarChart>
      </ResponsiveContainer>
      <span className="pointer-events-none absolute inset-0 grid place-items-center text-3xl font-semibold tabular-nums">
        {value}%
      </span>
      <span className="sr-only">Audit readiness score: {value} percent.</span>
    </div>
  );
}

/** Inject distribution across all 13 challenge dimensions. */
export function Donut({
  injects,
  onSelectDimension,
}: {
  injects: Inject[];
  onSelectDimension?: (dimension: string) => void;
}) {
  const counts = injects.reduce<Record<string, number>>((accumulator, inject) => {
    accumulator[inject.dimension] = (accumulator[inject.dimension] ?? 0) + 1;
    return accumulator;
  }, {});
  const groups = Object.entries(counts).map(([name, value]) => ({ name, value }));

  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={groups}
            dataKey="value"
            nameKey="name"
            innerRadius={58}
            outerRadius={96}
            paddingAngle={1}
            cursor={onSelectDimension ? "pointer" : undefined}
            onClick={onSelectDimension ? (_, index) => onSelectDimension(groups[index]?.name ?? "") : undefined}
          >
            {groups.map((group) => (
              <Cell key={group.name} fill={DIMENSION_COLORS[group.name as keyof typeof DIMENSION_COLORS]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption="Inject count by challenge dimension"
        headers={["Dimension", "Injects"]}
        rows={groups.map((group) => [group.name, group.value])}
      />
    </div>
  );
}

/** Evidence coverage per workflow area: complete, gap, and contradiction. */
export function EvidenceBars({ workflow }: { workflow: Workflow }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={workflow.evidenceByArea} margin={{ left: -16 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="area" tickLine={false} axisLine={false} />
          <YAxis width={32} tickLine={false} axisLine={false} />
          <Tooltip />
          <Legend />
          <Bar dataKey="complete" name="Complete" stackId="evidence" fill={SEMANTIC_COLORS.teal} />
          <Bar dataKey="gap" name="Gap" stackId="evidence" fill={SEMANTIC_COLORS.amber} />
          <Bar dataKey="contradiction" name="Contradiction" stackId="evidence" fill={SEMANTIC_COLORS.danger} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption={`Evidence coverage for ${workflow.name}`}
        headers={["Area", "Complete", "Gap", "Contradiction"]}
        rows={workflow.evidenceByArea.map((area) => [area.area, area.complete, area.gap, area.contradiction])}
      />
    </div>
  );
}

/** Radar of the 14 operating properties monitored for a workflow. */
export function OpsRadar({ workflow }: { workflow: Workflow }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart data={workflow.operatingProperties}>
          <PolarGrid />
          <PolarAngleAxis dataKey="label" tick={{ fontSize: 10 }} />
          <Radar dataKey="score" name="Score" stroke={SEMANTIC_COLORS.teal} fill={SEMANTIC_COLORS.teal} fillOpacity={0.25} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption={`Operating properties for ${workflow.name}`}
        headers={["Property", "Score"]}
        rows={workflow.operatingProperties.map((property) => [property.label, property.score])}
      />
    </div>
  );
}

/** Monthly model/inference spend, with the largest month-over-month spike flagged. */
export function CostArea({ data }: { data: KpiPoint[] }) {
  const spikeIndex = data.reduce((bestIndex, point, index) => {
    if (index === 0) return bestIndex;
    const increase = point.tokenCostUsd - data[index - 1].tokenCostUsd;
    const bestIncrease = bestIndex === -1 ? -Infinity : data[bestIndex].tokenCostUsd - data[bestIndex - 1].tokenCostUsd;
    return increase > bestIncrease ? index : bestIndex;
  }, -1);
  const spikePoint = spikeIndex >= 0 ? data[spikeIndex] : undefined;

  return (
    <div>
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={data} margin={{ left: -16, right: 16, top: 16 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" tickFormatter={(value: string) => value.slice(5)} tickLine={false} axisLine={false} />
          <YAxis width={48} tickLine={false} axisLine={false} tickFormatter={(value: number) => `$${value}`} />
          <Tooltip formatter={(value) => `$${Number(value ?? 0).toLocaleString()}`} />
          <Legend />
          <Area
            type="monotone"
            dataKey="tokenCostUsd"
            name="Model & token spend"
            stroke={SEMANTIC_COLORS.amber}
            fill={SEMANTIC_COLORS.amber}
            fillOpacity={0.18}
            strokeWidth={2}
          />
          <Area
            type="monotone"
            dataKey="inferenceCostUsd"
            name="Inference spend"
            stroke={SEMANTIC_COLORS.navy}
            fill={SEMANTIC_COLORS.navy}
            fillOpacity={0.12}
            strokeWidth={2}
          />
          {spikePoint && (
            <ReferenceDot
              x={spikePoint.date}
              y={spikePoint.tokenCostUsd}
              r={5}
              fill={SEMANTIC_COLORS.danger}
              stroke="white"
              label={{ value: "Spend spike flagged", position: "top", fill: SEMANTIC_COLORS.danger, fontSize: 11 }}
            />
          )}
        </AreaChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption="Monthly model and inference spend, in US dollars"
        headers={["Month", "Model & token spend", "Inference spend"]}
        rows={data.map((point) => [point.date, point.tokenCostUsd, point.inferenceCostUsd])}
      />
    </div>
  );
}

/** Fully-loaded operating cost broken down by category, as a horizontal bar. */
export function CostStacked({ data }: { data: CostPoint[] }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} layout="vertical" margin={{ left: 24, right: 24 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" tickFormatter={(value: number) => `$${(value / 1000).toFixed(1)}k`} tickLine={false} axisLine={false} />
          <YAxis type="category" dataKey="category" width={150} tickLine={false} axisLine={false} />
          <Tooltip formatter={(value) => `$${Number(value ?? 0).toLocaleString()}`} />
          <Bar dataKey="amount" radius={[0, 6, 6, 0]}>
            {data.map((point, index) => (
              <Cell key={point.category} fill={COST_BREAKDOWN_PALETTE[index % COST_BREAKDOWN_PALETTE.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption="Fully-loaded operating cost by category"
        headers={["Category", "Amount (USD)"]}
        rows={data.map((point) => [point.category, point.amount])}
      />
    </div>
  );
}

/** Inject counts stacked by status within each severity band. */
export function InjectStatusBar({ injects }: { injects: Inject[] }) {
  const rows = SEVERITY_ORDER.map((severity) => {
    const bucket = injects.filter((inject) => inject.severity === severity);
    return {
      severity,
      open: bucket.filter((inject) => inject.status === "open").length,
      mitigated: bucket.filter((inject) => inject.status === "mitigated").length,
      accepted: bucket.filter((inject) => inject.status === "accepted").length,
    };
  });

  return (
    <div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={rows} margin={{ left: -16 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="severity" tickLine={false} axisLine={false} className="capitalize" />
          <YAxis width={32} tickLine={false} axisLine={false} allowDecimals={false} />
          <Tooltip />
          <Legend />
          {STATUS_ORDER.map((status, index) => (
            <Bar
              key={status}
              dataKey={status}
              name={status}
              stackId="status"
              fill={STATUS_COLORS[status]}
              radius={index === STATUS_ORDER.length - 1 ? [4, 4, 0, 0] : undefined}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
      <SrOnlyTable
        caption="Inject status by severity"
        headers={["Severity", "Open", "Mitigated", "Accepted"]}
        rows={rows.map((row) => [row.severity, row.open, row.mitigated, row.accepted])}
      />
    </div>
  );
}

export { RiskHeatmap } from "@/components/charts/risk-heatmap";
export { PvFunnel } from "@/components/charts/pv-funnel";
