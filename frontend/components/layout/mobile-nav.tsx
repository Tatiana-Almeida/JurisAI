"use client";

import Link from "next/link";
import { Menu } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { NAVIGATION_ITEMS } from "@/lib/constants/navigation";

export function MobileNav() {
  return (
    <Sheet>
      <SheetTrigger asChild className="lg:hidden">
        <Button variant="outline" size="icon" className="rounded-full">
          <Menu className="size-4" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-80">
        <SheetHeader>
          <SheetTitle>JurisAI</SheetTitle>
        </SheetHeader>
        <div className="mt-6 grid gap-2">
          {NAVIGATION_ITEMS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className="rounded-2xl border border-border/60 px-4 py-3 text-sm font-medium"
            >
              {label}
            </Link>
          ))}
        </div>
      </SheetContent>
    </Sheet>
  );
}
