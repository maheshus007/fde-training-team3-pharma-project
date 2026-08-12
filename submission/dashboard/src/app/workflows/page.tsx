"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { FadeIn } from "@/components/motion/fade-in";
import { useFilters } from "@/components/providers/filter-provider";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tracker, type TrackerDatum } from "@/components/ui/tracker";
import { getDashboardData } from "@/lib/data";

export default function WorkflowsPage() {
  const data = getDashboardData(useFilters());

  return (
    <div className="space-y-6">
      <FadeIn>
        <div>
          <h1 className="text-3xl font-semibold">Supported workflows</h1>
          <p className="mt-2 max-w-2xl text-muted-foreground">
            Evidence preparation and routing support only; accountable people retain every regulated decision.
          </p>
        </div>
      </FadeIn>

      <div className="grid gap-4 lg:grid-cols-3">
        {data.workflows.map((workflow, index) => {
          const trackerData: TrackerDatum[] = workflow.tracker.map((run, runIndex) => ({
            key: runIndex,
            status: run,
          }));

          return (
            <FadeIn key={workflow.id} delay={index * 0.05}>
              <Card className="h-full rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-lg">{workflow.name}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-emerald-600">Supports</p>
                    <ul className="mt-1 list-disc space-y-0.5 pl-4 text-sm text-muted-foreground">
                      {workflow.supports.slice(0, 2).map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <p className="text-sm font-medium text-amber-600">Never</p>
                    <p className="text-sm text-muted-foreground">{workflow.neverDoes[0]}</p>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Contract tests passing</span>
                      <b className="text-foreground">{workflow.contractsPassing}%</b>
                    </div>
                    <Progress value={workflow.contractsPassing} className="mt-1.5" />
                  </div>

                  <div>
                    <p className="mb-1.5 text-xs text-muted-foreground">Recent run history</p>
                    <Tracker data={trackerData} />
                  </div>

                  <Link
                    className="inline-flex items-center gap-1 pt-1 text-sm font-medium text-primary hover:underline"
                    href={`/workflows/${workflow.id}`}
                  >
                    Open workflow detail <ArrowRight className="size-3.5" />
                  </Link>
                </CardContent>
              </Card>
            </FadeIn>
          );
        })}
      </div>
    </div>
  );
}
