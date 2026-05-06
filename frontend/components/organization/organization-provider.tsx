"use client";

import { useEffect, useRef } from "react";
import { clearTenantCache, invalidateOrganizationScopedQueries, queryClient } from "@/lib/query/query-client";
import { useOrganizationStore } from "@/stores/organization-store";

type OrganizationProviderProps = {
  children: React.ReactNode;
};

export function OrganizationProvider({ children }: OrganizationProviderProps) {
  const activeOrganizationId = useOrganizationStore((state) => state.activeOrganizationId);
  const previousOrganizationIdRef = useRef<string | null>(null);

  useEffect(() => {
    const previousOrganizationId = previousOrganizationIdRef.current;

    if (
      previousOrganizationId &&
      activeOrganizationId &&
      previousOrganizationId !== activeOrganizationId
    ) {
      clearTenantCache(queryClient, previousOrganizationId);
      invalidateOrganizationScopedQueries(queryClient, activeOrganizationId);
    }

    previousOrganizationIdRef.current = activeOrganizationId;
  }, [activeOrganizationId]);

  return children;
}
