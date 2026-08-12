import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { InjectStatus, Severity } from "@/lib/schemas";

const SEVERITY_STYLES: Record<Severity, string> = {
  critical: "border-transparent bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-300",
  high: "border-transparent bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  medium: "border-transparent bg-sky-100 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300",
  low: "border-transparent bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
};

const STATUS_STYLES: Record<InjectStatus, string> = {
  open: "border-transparent bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-300",
  mitigated: "border-transparent bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  accepted: "border-transparent bg-slate-100 text-slate-700 dark:bg-slate-800/60 dark:text-slate-300",
};

export function SeverityBadge({ severity, className }: { severity: Severity; className?: string }) {
  return (
    <Badge variant="outline" className={cn("capitalize", SEVERITY_STYLES[severity], className)}>
      {severity}
    </Badge>
  );
}

export function StatusBadge({ status, className }: { status: InjectStatus; className?: string }) {
  return (
    <Badge variant="outline" className={cn("capitalize", STATUS_STYLES[status], className)}>
      {status}
    </Badge>
  );
}
