"use client";

import { ChartCard } from "@/components/cards/chart-card";
import { MetricCard } from "@/components/cards/metric-card";
import { CostArea, CostStacked } from "@/components/charts/dashboard-charts";
import { FadeIn } from "@/components/motion/fade-in";
import { useFilters } from "@/components/providers/filter-provider";
import { currency } from "@/lib/format";
import { getDashboardData } from "@/lib/data";

export default function EconomicsPage() {
  const { economics, kpis } = getDashboardData(useFilters());
  const roiMultiple = (economics.costAvoidanceUsd / (economics.costPerTaskUsd * economics.tasksCompleted)).toFixed(1);

  return (
    <div className="space-y-6">
      <FadeIn>
        <div>
          <h1 className="text-3xl font-semibold">Value &amp; FinOps</h1>
          <p className="mt-2 max-w-2xl text-muted-foreground">
            Every dollar avoided is tracked alongside the human-review share it protects, so cost efficiency is
            never read apart from its safety controls.
          </p>
        </div>
      </FadeIn>

      <FadeIn delay={0.05}>
        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            label="Cost per task"
            value={currency(economics.costPerTaskUsd)}
            delta={`${economics.budgetVariancePercent}% to budget`}
            favorable={economics.budgetVariancePercent <= 0}
            spark={kpis.map((point) => point.tokenCostUsd)}
          />
          <MetricCard
            label="Avoided inference cost"
            value={currency(economics.costAvoidanceUsd)}
            delta="+$4,200 vs. last period"
            favorable
          />
          <MetricCard
            label="Human review share"
            value={`${economics.humanReviewSharePercent}%`}
            delta="Accountable oversight retained"
            favorable
          />
          <MetricCard
            label="Tasks completed"
            value={economics.tasksCompleted.toLocaleString()}
            delta={`${economics.reviewerHoursSaved.toLocaleString()} reviewer hours saved`}
            favorable
          />
        </section>
      </FadeIn>

      <FadeIn delay={0.1}>
        <section className="grid gap-4 lg:grid-cols-2">
          <ChartCard
            title="Cost trend"
            subtitle="Model and inference spend by month"
            why="Budget spikes are visible, flagged controls, not silent service degradation."
          >
            <CostArea data={kpis} />
          </ChartCard>
          <ChartCard
            title="Fully-loaded cost of operations"
            why="Total operating cost includes control and review effort, not model spend alone."
          >
            <CostStacked data={economics.costBreakdown} />
          </ChartCard>
        </section>
      </FadeIn>

      <FadeIn delay={0.15}>
        <section className="rounded-2xl bg-emerald-600 p-6 text-white">
          <h2 className="text-xl font-semibold">ROI callout</h2>
          <p className="mt-2 max-w-3xl">
            The portfolio has avoided {currency(economics.costAvoidanceUsd)} of unnecessary inference &mdash; roughly
            a {roiMultiple}&times; return on task-level spend &mdash; while preserving human review for every
            regulated judgment.
          </p>
        </section>
      </FadeIn>
    </div>
  );
}
