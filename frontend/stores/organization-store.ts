"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Organization } from "@/types/organization";

type OrganizationLoadStatus = "idle" | "loading" | "ready" | "error";

type OrganizationState = {
  activeOrganizationId: string | null;
  availableOrganizations: Organization[];
  loadStatus: OrganizationLoadStatus;
  loadError: string | null;
  setLoading: () => void;
  setLoadError: (message: string) => void;
  clearLoadError: () => void;
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
      loadStatus: "idle",
      loadError: null,
      setLoading: () =>
        set({
          loadStatus: "loading",
          loadError: null,
        }),
      setLoadError: (message) =>
        set({
          availableOrganizations: [],
          activeOrganizationId: null,
          loadStatus: "error",
          loadError: message,
        }),
      clearLoadError: () =>
        set((state) => ({
          loadStatus: state.availableOrganizations.length > 0 ? "ready" : "idle",
          loadError: null,
        })),
      setAvailableOrganizations: (organizations) =>
        set((state) => ({
          availableOrganizations: organizations,
          loadStatus: organizations.length > 0 ? "ready" : "idle",
          loadError: null,
          activeOrganizationId:
            state.activeOrganizationId &&
            organizations.some((item) => item.id === state.activeOrganizationId)
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
            loadStatus: organizations.length > 0 ? "ready" : "idle",
            loadError: null,
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
          loadStatus: "idle",
          loadError: null,
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
