"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, Search, UserCircle2 } from "lucide-react";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { MobileNav } from "@/components/layout/mobile-nav";
import { OrganizationSwitcher } from "@/components/organization/organization-switcher";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Input } from "@/components/ui/input";
import { NAVIGATION_ITEMS } from "@/lib/constants/navigation";

function buildBreadcrumbs(pathname: string) {
  const currentItem = NAVIGATION_ITEMS.find((item) => pathname === item.href || pathname.startsWith(`${item.href}/`));

  if (!currentItem || currentItem.href === "/dashboard") {
    return [];
  }

  return [
    { label: "Dashboard", href: "/dashboard" },
    { label: currentItem.label, href: currentItem.href },
  ];
}

export function Topbar() {
  const pathname = usePathname();
  const { activeOrganization } = useActiveOrganization();
  const breadcrumbs = buildBreadcrumbs(pathname);

  return (
    <header className="sticky top-0 z-30 border-b border-border/60 bg-background/85 backdrop-blur-md">
      <div className="flex flex-col gap-3 px-4 py-4 sm:px-6">
        <div className="flex items-center gap-3">
          <MobileNav />
          <div className="hidden min-w-0 flex-1 items-center gap-3 md:flex">
            <div className="relative max-w-md flex-1">
              <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Busca global em preparacao"
                className="rounded-full border-border/70 bg-background/80 pl-9"
              />
            </div>
          </div>
          <div className="min-w-0">
            <OrganizationSwitcher />
          </div>
          <div className="ml-auto flex items-center gap-2">
            <ThemeToggle />
            <button
              type="button"
              className="rounded-full border border-border/70 bg-background/80 p-2 text-muted-foreground"
              aria-label="Notificacoes em preparacao"
            >
              <Bell className="size-4" />
            </button>
            <button
              type="button"
              className="rounded-full border border-border/70 bg-background/80 p-2 text-muted-foreground"
              aria-label="Perfil do utilizador"
            >
              <UserCircle2 className="size-4" />
            </button>
          </div>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-muted-foreground">
          <div className="flex flex-wrap items-center gap-2">
            <span>Tenant ativo:</span>
            <span className="rounded-full bg-primary/10 px-3 py-1 text-primary">
              {activeOrganization?.name ?? "nao selecionado"}
            </span>
          </div>
          {breadcrumbs.length > 0 ? (
            <nav aria-label="Breadcrumb" className="flex flex-wrap items-center gap-2">
              {breadcrumbs.map((breadcrumb, index) => (
                <span key={breadcrumb.href} className="flex items-center gap-2">
                  {index > 0 ? <span>/</span> : null}
                  <Link href={breadcrumb.href} className="hover:text-foreground">
                    {breadcrumb.label}
                  </Link>
                </span>
              ))}
            </nav>
          ) : null}
        </div>
      </div>
    </header>
  );
}
