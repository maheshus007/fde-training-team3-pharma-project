"use client";

import { BarList, type BarListItem } from "@/components/charts/bar-list";
import { AuditRadial, LeadTimeArea } from "@/components/charts/dashboard-charts";
import { RiskHeatmap } from "@/components/charts/risk-heatmap";
import { ChartCard } from "@/components/cards/chart-card";
import { MetricCard } from "@/components/cards/metric-card";
import { FadeIn } from "@/components/motion/fade-in";
import { Badge } from "@/components/ui/badge";
import { useFilters } from "@/components/providers/filter-provider";
import { getDashboardData } from "@/lib/data";

const IMPACT_WEIGHT: Record<string, number> = { High: 3, Medium: 2, Low: 1 };

export default function Home() {
  const filters = useFilters();
  const data = getDashboardData(filters);
  const snapshot = data.snapshot;

  const gapItems: BarListItem[] = snapshot.topGaps.map((gap) => ({
    label: gap.name,
    value: IMPACT_WEIGHT[gap.impact] ?? 1,
    valueLabel: gap.impact,
    description: gap.value,
  }));

  return (
    <div className="space-y-6">
      <FadeIn>
        <section>
          <p className="text-sm font-medium text-primary">Executive overview</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Decision Cockpit</h1>
          <p className="mt-1 max-w-2xl text-sm text-muted-foreground">
            A single view of release speed, evidence quality, and value across the three AEGIS-PHARMA supported workflows.
          </p>
        </section>
      </FadeIn>

      <FadeIn delay={0.05}>
        <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5 dark:border-emerald-900 dark:bg-emerald-950/30">
          <div className="flex flex-wrap items-center gap-2">
            <Badge className="bg-emerald-600 px-3 py-1 text-sm text-white">{snapshot.decisionState}</Badge>
            <span className="text-sm">{snapshot.decisionRationale}</span>
          </div>
          <p className="mt-3 font-medium">Requested decision: {snapshot.requestedDecision}</p>
          <div className="mt-3 flex flex-wrap gap-2 text-xs">
            <span className="rounded-full bg-card px-2 py-1">Supports 3 workflows</span>
            <span className="rounded-full bg-card px-2 py-1">Executes 0 regulated decisions</span>
            <span className="rounded-full bg-card px-2 py-1">Reproducible &amp; offline</span>
          </div>
        </section>
      </FadeIn>

      <FadeIn delay={0.1}>
        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {snapshot.kpis.map((kpi) => (
            <MetricCard key={kpi.label} {...kpi} />
          ))}
        </section>
      </FadeIn>

      <FadeIn delay={0.15}>
        <section className="grid gap-4 lg:grid-cols-2">
          <ChartCard
            title="Release lead-time"
            subtitle="Are we getting faster without cutting corners?"
            why="A declining lead-time only matters when evidence and approval controls remain intact."
          >
            <LeadTimeArea data={data.kpis} />
          </ChartCard>
          <ChartCard
            title="Audit readiness"
            why="Readiness surfaces whether cited evidence is fit for accountable review."
          >
            <AuditRadial value={snapshot.auditReadiness} />
          </ChartCard>
        </section>
      </FadeIn>

      <FadeIn delay={0.2}>
        <ChartCard
          title="Risk heatmap"
          subtitle="Inject concentration across all 13 challenge dimensions"
          why="Concentrated high-severity injects guide oversight and resilience work; open the Evidence & Risk page to filter and drill in."
        >
          <RiskHeatmap data={data.heatmap} />
        </ChartCard>
      </FadeIn>

      <FadeIn delay={0.25}>
        <ChartCard
          title="Top evidence gaps"
          subtitle="Ranked by business impact"
          why="Open gaps are explicit conditions for accountable human owners, not items the system resolves on its own."
        >
          <BarList data={gapItems} />
        </ChartCard>
      </FadeIn>

      <FadeIn delay={0.3}>
        <section className="rounded-2xl border bg-card p-6">
          <h2 className="text-lg font-semibold">Executive summary</h2>
          <p className="mt-2 max-w-4xl text-muted-foreground">{snapshot.executiveSummary}</p>
        </section>
      </FadeIn>
    </div>
  );
}
