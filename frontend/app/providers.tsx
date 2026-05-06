"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";
import { OrganizationProvider } from "@/components/organization/organization-provider";
import { queryClient } from "@/lib/query/query-client";

type ProvidersProps = {
  children: React.ReactNode;
};

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <QueryClientProvider client={queryClient}>
        <OrganizationProvider>
          {children}
          <Toaster richColors position="top-right" />
        </OrganizationProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
}
