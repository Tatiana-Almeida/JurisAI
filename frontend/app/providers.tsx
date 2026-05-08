"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";
import { OrganizationProvider } from "@/components/organization/organization-provider";
import { useAuthBootstrap } from "@/hooks/use-auth-bootstrap";
import { queryClient } from "@/lib/query/query-client";

type ProvidersProps = {
  children: React.ReactNode;
};

function AuthBootstrap() {
  useAuthBootstrap();
  return null;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <QueryClientProvider client={queryClient}>
        <OrganizationProvider>
          <AuthBootstrap />
          {children}
          <Toaster richColors position="top-right" />
        </OrganizationProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
}
