"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  CircleDollarSign,
  LayoutDashboard,
  ShieldAlert,
  ShieldCheck,
  Workflow,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

const items = [
  { label: "Overview", href: "/", icon: LayoutDashboard },
  { label: "Workflows", href: "/workflows", icon: Workflow },
  { label: "Evidence & Risk", href: "/risk", icon: ShieldAlert },
  { label: "Governance", href: "/governance", icon: ShieldCheck },
  { label: "Value & FinOps", href: "/economics", icon: CircleDollarSign },
  { label: "Glossary", href: "/about", icon: BookOpen },
];

export function AppSidebar() {
  const path = usePathname();

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="gap-1 p-5">
        <span className="text-sm font-bold tracking-[0.14em] text-sidebar-primary">
          AEGIS-PHARMA
        </span>
        <span className="text-xs text-sidebar-foreground/70">NovaCura Therapeutics</span>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map(({ label, href, icon: Icon }) => {
                const active = path === href || (href !== "/" && path.startsWith(href));
                return (
                  <SidebarMenuItem key={href}>
                    <SidebarMenuButton asChild isActive={active} tooltip={label}>
                      <Link href={href}>
                        <Icon />
                        <span>{label}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="p-4 text-xs text-sidebar-foreground/60">
        AI supports · humans decide
      </SidebarFooter>
    </Sidebar>
  );
}
