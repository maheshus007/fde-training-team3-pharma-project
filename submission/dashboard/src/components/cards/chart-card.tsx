import { Info } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export function ChartCard({
  title,
  subtitle,
  tooltip,
  why,
  className,
  children,
}: {
  title: string;
  subtitle?: string;
  tooltip?: string;
  why: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <Card className={`rounded-2xl border-border/80 shadow-sm ${className ?? ""}`}>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-base">
          {title}
          {tooltip && (
            <Tooltip>
              <TooltipTrigger aria-label={`About ${title}`}>
                <Info className="size-4 text-muted-foreground" />
              </TooltipTrigger>
              <TooltipContent>{tooltip}</TooltipContent>
            </Tooltip>
          )}
        </CardTitle>
        {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
      </CardHeader>
      <CardContent>
        <div className="relative min-h-[220px] w-full min-w-0">{children}</div>
        <p className="mt-4 border-t pt-3 text-xs text-muted-foreground">
          <b>Why it matters:</b> {why}
        </p>
      </CardContent>
    </Card>
  );
}
