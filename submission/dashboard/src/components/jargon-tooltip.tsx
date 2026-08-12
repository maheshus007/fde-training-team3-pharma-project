"use client";

import { glossary, type GlossaryTerm } from "@/lib/glossary";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export function JargonTooltip({ term, children }: { term: GlossaryTerm; children?: React.ReactNode }) {
  const definition = glossary[term];
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button
          type="button"
          className="underline decoration-dotted underline-offset-4 hover:text-primary"
        >
          {children ?? term}
        </button>
      </TooltipTrigger>
      <TooltipContent className="max-w-xs text-sm">{definition}</TooltipContent>
    </Tooltip>
  );
}
