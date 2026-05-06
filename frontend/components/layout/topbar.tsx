"use client";

import { Bell, Search, UserCircle2 } from "lucide-react";
import { OrganizationSwitcher } from "@/components/organization/organization-switcher";
import { MobileNav } from "@/components/layout/mobile-nav";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Input } from "@/components/ui/input";

export function Topbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-border/60 bg-background/85 backdrop-blur-md">
      <div className="flex items-center gap-3 px-4 py-4 sm:px-6">
        <MobileNav />
        <div className="hidden flex-1 items-center gap-3 md:flex">
          <div className="relative max-w-md flex-1">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Busca global (placeholder)"
              className="rounded-full border-border/70 bg-background/80 pl-9"
            />
          </div>
        </div>
        <OrganizationSwitcher />
        <div className="ml-auto flex items-center gap-2">
          <ThemeToggle />
          <div className="rounded-full border border-border/70 bg-background/80 p-2 text-muted-foreground">
            <Bell className="size-4" />
          </div>
          <div className="rounded-full border border-border/70 bg-background/80 p-2 text-muted-foreground">
            <UserCircle2 className="size-4" />
          </div>
        </div>
      </div>
    </header>
  );
}
