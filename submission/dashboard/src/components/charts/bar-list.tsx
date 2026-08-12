import { cn } from "@/lib/utils";

export type BarListItem = {
  label: string;
  value: number;
  valueLabel?: string;
  description?: string;
};

/**
 * A polished, dependency-free stand-in for Tremor's BarList: horizontal
 * bars scaled to the largest value, with an optional badge and caption.
 */
export function BarList({ data, barClassName }: { data: BarListItem[]; barClassName?: string }) {
  const max = Math.max(...data.map((item) => item.value), 1);

  return (
    <ul className="space-y-4">
      {data.map((item) => (
        <li key={item.label}>
          <div className="flex items-center justify-between gap-3 text-sm">
            <span className="font-medium">{item.label}</span>
            {item.valueLabel && <span className="shrink-0 text-xs font-semibold text-amber-600">{item.valueLabel}</span>}
          </div>
          <div className="mt-1.5 h-2 w-full overflow-hidden rounded-full bg-muted">
            <div
              className={cn("h-full rounded-full bg-primary", barClassName)}
              style={{ width: `${(item.value / max) * 100}%` }}
            />
          </div>
          {item.description && <p className="mt-1 text-xs text-muted-foreground">{item.description}</p>}
        </li>
      ))}
    </ul>
  );
}
