"use client";

import { notFound, useParams } from "next/navigation";

import { ChartCard } from "@/components/cards/chart-card";
import { EvidenceBars, OpsRadar } from "@/components/charts/dashboard-charts";
import { PvFunnel } from "@/components/charts/pv-funnel";
import { FadeIn } from "@/components/motion/fade-in";
import { Badge } from "@/components/ui/badge";
import { workflows } from "@/lib/data";

const SAMPLE_OUTPUT_LABELS: Record<string, string> = {
  cited: "Cited evidence",
  contradictions: "Contradictions found",
  gaps: "Open gaps",
  humanReviews: "Required human reviews",
};

export default function WorkflowDetail() {
  const { id } = useParams<{ id: string }>();
  const workflow = workflows.find((item) => item.id === id);

  if (!workflow) return notFound();

  return (
    <div className="space-y-6">
      <FadeIn>
        <div>
          <p className="text-sm text-primary">Workflow boundary</p>
          <h1 className="text-3xl font-semibold">{workflow.name}</h1>
        </div>
      </FadeIn>

      <FadeIn delay={0.05}>
        <section className="grid gap-4 lg:grid-cols-2">
          <ChartCard
            title="Operating properties"
            why="All 14 properties are monitored continuously to preserve bounded, reproducible workflow behaviour."
          >
            <OpsRadar workflow={workflow} />
          </ChartCard>
          <ChartCard
            title="Evidence coverage"
            why="Gaps and contradictions route to accountable humans rather than being silently resolved."
          >
            <EvidenceBars workflow={workflow} />
          </ChartCard>
        </section>
      </FadeIn>

      {workflow.id === "pv" && workflow.funnelStages && (
        <FadeIn delay={0.1}>
          <ChartCard
            title="Case prioritisation funnel"
            subtitle="Case volume narrows as evidence, signal, and medical review accumulate"
            why="A shrinking funnel with visible drop-off shows where reviewer time is concentrated, without the system deciding seriousness on its own."
          >
            <PvFunnel stages={workflow.funnelStages} />
          </ChartCard>
        </FadeIn>
      )}

      <FadeIn delay={0.15}>
        <section className="rounded-2xl border bg-card p-5">
          <h2 className="font-semibold">Contract-test panel</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Positive tests confirm supported behaviour; prohibited tests confirm regulated actions stay blocked.
          </p>
          <div className="mt-3 grid gap-2">
            {workflow.contractTests.map((test) => (
              <div key={test.id} className="flex items-center justify-between rounded-lg bg-muted/50 p-3 text-sm">
                <span>
                  <span className="font-mono text-xs text-muted-foreground">{test.id}</span> &middot; {test.name}
                </span>
                <Badge
                  variant="outline"
                  className="border-transparent bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300"
                >
                  {test.kind === "prohibited" ? "Correctly blocked" : "Pass"}
                </Badge>
              </div>
            ))}
          </div>
        </section>
      </FadeIn>

      <FadeIn delay={0.2}>
        <section className="rounded-2xl border bg-card p-5">
          <h2 className="font-semibold">Sample reviewer-ready output</h2>
          <div className="mt-3 grid gap-4 text-sm md:grid-cols-2">
            {Object.entries(workflow.sampleOutput).map(([key, items]) => (
              <div key={key}>
                <b>{SAMPLE_OUTPUT_LABELS[key] ?? key}</b>
                <ul className="mt-1 list-disc space-y-0.5 pl-5 text-muted-foreground">
                  {items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      </FadeIn>
    </div>
  );
}
