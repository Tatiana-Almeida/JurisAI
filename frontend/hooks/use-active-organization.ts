"use client";

import { useMemo } from "react";
import { useOrganizationStore } from "@/stores/organization-store";

export function useActiveOrganization() {
  const activeOrganizationId = useOrganizationStore((state) => state.activeOrganizationId);
  const availableOrganizations = useOrganizationStore((state) => state.availableOrganizations);

  const activeOrganization = useMemo(
    () =>
      availableOrganizations.find((organization) => organization.id === activeOrganizationId) ??
      null,
    [activeOrganizationId, availableOrganizations],
  );

  return {
    activeOrganization,
    activeOrganizationId,
    availableOrganizations,
  };
}
