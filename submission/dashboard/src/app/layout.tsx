import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Suspense } from "react";
import "./globals.css";
import { ThemeProvider } from "@/components/providers/theme-provider";
import { FilterProvider } from "@/components/providers/filter-provider";
import { AppShell } from "@/components/layout/app-shell";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AEGIS-PHARMA Decision Cockpit",
  description:
    "Executive and operations decision-support dashboard for NovaCura Therapeutics. AI supports; humans decide.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <ThemeProvider>
          <TooltipProvider>
            <Suspense fallback={<main className="p-8 text-sm text-muted-foreground">Loading decision cockpit…</main>}>
              <FilterProvider>
                <AppShell>{children}</AppShell>
                <Toaster />
              </FilterProvider>
            </Suspense>
          </TooltipProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
