import { ArrowDownRight, ArrowUpRight } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";

function buildSparkPoints(spark: number[]): string {
  if (spark.length === 0) return "";
  const min = Math.min(...spark);
  const max = Math.max(...spark);
  const range = Math.max(1, max - min);
  return spark
    .map((value, index) => {
      const x = index * (100 / Math.max(1, spark.length - 1));
      const y = 34 - ((value - min) / range) * 28;
      return `${x},${y}`;
    })
    .join(" ");
}

export function MetricCard({
  label,
  value,
  delta,
  favorable = true,
  spark = [],
}: {
  label: string;
  value: string;
  delta: string;
  favorable?: boolean;
  spark?: number[];
}) {
  const points = buildSparkPoints(spark);

  return (
    <Card className="rounded-2xl">
      <CardContent className="p-5">
        <p className="text-sm text-muted-foreground">{label}</p>
        <div className="mt-2 flex items-end justify-between gap-3">
          <div>
            <p className="tabular-nums text-2xl font-semibold tracking-tight">{value}</p>
            <p className={`mt-1 flex items-center text-xs font-medium ${favorable ? "text-emerald-600" : "text-destructive"}`}>
              {favorable ? <ArrowUpRight className="mr-1 size-3" /> : <ArrowDownRight className="mr-1 size-3" />}
              {delta}
            </p>
          </div>
          {points && (
            <svg viewBox="0 0 100 40" aria-label={`${label} trend`} className="h-10 w-24 overflow-visible">
              <polyline points={points} fill="none" stroke="var(--chart-1)" strokeWidth="3" strokeLinecap="round" />
            </svg>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
