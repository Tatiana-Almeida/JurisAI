"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Organization } from "@/types/organization";

type OrganizationState = {
  activeOrganizationId: string | null;
  availableOrganizations: Organization[];
  setAvailableOrganizations: (organizations: Organization[]) => void;
  bootstrapOrganizations: (organizations: Organization[]) => void;
  setActiveOrganization: (organizationId: string | null) => void;
  reset: () => void;
};

export const useOrganizationStore = create<OrganizationState>()(
  persist(
    (set) => ({
      activeOrganizationId: null,
      availableOrganizations: [],
      setAvailableOrganizations: (organizations) =>
        set((state) => ({
          availableOrganizations: organizations,
          activeOrganizationId:
            state.activeOrganizationId && organizations.some((item) => item.id === state.activeOrganizationId)
              ? state.activeOrganizationId
              : organizations[0]?.id ?? null,
        })),
      bootstrapOrganizations: (organizations) =>
        set((state) => {
          const persistedExists =
            state.activeOrganizationId &&
            organizations.some((item) => item.id === state.activeOrganizationId);

          return {
            availableOrganizations: organizations,
            activeOrganizationId: persistedExists
              ? state.activeOrganizationId
              : organizations.length === 1
                ? organizations[0]?.id ?? null
                : null,
          };
        }),
      setActiveOrganization: (organizationId) =>
        set({
          activeOrganizationId: organizationId,
        }),
      reset: () =>
        set({
          activeOrganizationId: null,
          availableOrganizations: [],
        }),
    }),
    {
      name: "jurisai.organization-store",
      partialize: (state) => ({
        activeOrganizationId: state.activeOrganizationId,
      }),
    },
  ),
);
