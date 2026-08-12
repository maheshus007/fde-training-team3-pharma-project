import { cn } from "@/lib/utils";

export type TrackerStatus = "pass" | "abstain" | "blocked";

export type TrackerDatum = {
  key: string | number;
  status: TrackerStatus;
  label?: string;
};

const STATUS_STYLES: Record<TrackerStatus, string> = {
  pass: "bg-emerald-500",
  abstain: "bg-slate-400",
  blocked: "bg-amber-500",
};

const STATUS_LABELS: Record<TrackerStatus, string> = {
  pass: "Passed",
  abstain: "Abstained",
  blocked: "Blocked",
};

/** A row of coloured segments summarising recent run outcomes, à la Tremor's Tracker. */
export function Tracker({ data, className }: { data: TrackerDatum[]; className?: string }) {
  return (
    <div
      className={cn("flex gap-1", className)}
      role="img"
      aria-label={`Recent run history: ${data.map((datum) => STATUS_LABELS[datum.status]).join(", ")}`}
    >
      {data.map((datum) => (
        <span
          key={datum.key}
          title={datum.label ?? STATUS_LABELS[datum.status]}
          className={cn("h-2 flex-1 rounded-full", STATUS_STYLES[datum.status])}
        />
      ))}
    </div>
  );
}
