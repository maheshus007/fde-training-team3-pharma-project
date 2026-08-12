"use client";

import { Check, X } from "lucide-react";

import { FadeIn } from "@/components/motion/fade-in";
import { JargonTooltip } from "@/components/jargon-tooltip";
import { useFilters } from "@/components/providers/filter-provider";
import { Progress } from "@/components/ui/progress";
import { getDashboardData } from "@/lib/data";

export default function GovernancePage() {
  const governance = getDashboardData(useFilters()).governance;

  return (
    <div className="space-y-6">
      <FadeIn>
        <div>
          <h1 className="text-3xl font-semibold">Governance &amp; boundaries</h1>
          <p className="mt-2 max-w-2xl text-muted-foreground">
            Every <JargonTooltip term="bounded workflow" /> is fail-closed by design: when identity, authority,
            units, or timing cannot be verified, AEGIS-PHARMA records an <JargonTooltip term="abstention" /> instead
            of guessing.
          </p>
        </div>
      </FadeIn>

      <FadeIn delay={0.05}>
        <section className="grid gap-4 lg:grid-cols-2">
          <div className="rounded-2xl border border-emerald-200 bg-card p-5">
            <h2 className="font-semibold text-emerald-700">What AEGIS supports</h2>
            <ul className="mt-3 space-y-2 text-sm">
              {governance.boundaryDoes.map((item) => (
                <li key={item} className="flex items-start gap-2">
                  <Check className="mt-0.5 size-4 shrink-0 text-emerald-600" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-amber-200 bg-card p-5">
            <h2 className="font-semibold text-amber-700">What it never executes</h2>
            <ul className="mt-3 space-y-2 text-sm">
              {governance.boundaryNever.map((item) => (
                <li key={item} className="flex items-start gap-2">
                  <X className="mt-0.5 size-4 shrink-0 text-amber-600" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </FadeIn>

      <FadeIn delay={0.1}>
        <section className="rounded-2xl border bg-card p-5">
          <h2 className="font-semibold">Hard gates</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Fail-closed controls that stop a workflow rather than proceed on unverifiable evidence.
          </p>
          <div className="mt-3 grid gap-2">
            {governance.hardGates.map((gate) => (
              <div key={gate.id} className="flex items-center justify-between gap-4 rounded-lg bg-muted/50 p-3 text-sm">
                <span>
                  {gate.label}
                  <small className="block text-muted-foreground">{gate.detail}</small>
                </span>
                <b className="shrink-0 text-emerald-600">{gate.pass ? "Pass" : "Fail"}</b>
              </div>
            ))}
          </div>
        </section>
      </FadeIn>

      <FadeIn delay={0.15}>
        <section className="rounded-2xl border bg-card p-5">
          <h2 className="font-semibold">Continuity controls</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Readiness to keep operating &mdash; manually, if required &mdash; if AI support is disabled.
          </p>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            {governance.continuityMetrics.map((metric) => (
              <div key={metric.label}>
                <div className="flex justify-between text-sm">
                  <span>{metric.label}</span>
                  <b>{metric.score}%</b>
                </div>
                <Progress value={metric.score} className="mt-2" />
              </div>
            ))}
          </div>
        </section>
      </FadeIn>

      <FadeIn delay={0.2}>
        <p className="rounded-2xl bg-primary p-5 text-primary-foreground">
          <b>Bounded AI, plainly:</b> the system prepares cited evidence and routes uncertainty. It cannot take a
          regulated decision, and it stops when required authority or evidence cannot be verified.
        </p>
      </FadeIn>
    </div>
  );
}
