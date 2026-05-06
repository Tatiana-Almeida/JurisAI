"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { clearTenantCache, invalidateOrganizationScopedQueries, queryClient } from "@/lib/query/query-client";
import { useOrganizationStore } from "@/stores/organization-store";

type OrganizationProviderProps = {
  children: React.ReactNode;
};

export function OrganizationProvider({ children }: OrganizationProviderProps) {
  const router = useRouter();
  const activeOrganizationId = useOrganizationStore((state) => state.activeOrganizationId);
  const previousOrganizationIdRef = useRef<string | null>(null);

  useEffect(() => {
    const previousOrganizationId = previousOrganizationIdRef.current;

    if (
      previousOrganizationId &&
      activeOrganizationId &&
      previousOrganizationId !== activeOrganizationId
    ) {
      queryClient.clear();
      clearTenantCache(queryClient, previousOrganizationId);
      invalidateOrganizationScopedQueries(queryClient, activeOrganizationId);
      router.replace("/dashboard");
    }

    previousOrganizationIdRef.current = activeOrganizationId;
  }, [activeOrganizationId, router]);

  return children;
}
