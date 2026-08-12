# AEGIS-PHARMA Decision Cockpit

Executive and operations decision-support UI for NovaCura Therapeutics.
The dashboard prepares and visualises evidence; it does **not** execute regulated decisions.

## Stack

- Next.js 15 (App Router) · React 19 · TypeScript
- Tailwind CSS v4 · shadcn/ui
- Recharts (default charts) · ApexCharts (heatmap + PV funnel) · Tremor-compatible metric patterns
- TanStack Table v8 · next-themes · framer-motion · zod

## Run locally

```bash
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

If `pnpm` is unavailable:

```bash
corepack enable
corepack prepare pnpm@latest --activate
```

## Production validation

```bash
pnpm build
pnpm start
```

## Routes

| Route | Purpose |
|---|---|
| `/` | Executive overview (Conditional-Go) |
| `/workflows` · `/workflows/[id]` | Bounded Batch / PV / Supply workflows |
| `/risk` | 84 injects, heatmap, TanStack table |
| `/governance` | Safety boundary & hard gates |
| `/economics` | Value & FinOps |
| `/about` | Glossary & how to read |

Product and time-range filters in the top bar sync to URL search params and apply across pages.

Mock data lives in `src/lib/data/` and is also exposed via `/api/*` route handlers (`USE_MOCK = true` in `src/lib/config.ts`).
