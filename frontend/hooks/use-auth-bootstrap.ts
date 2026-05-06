"use client";

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { endpoints } from "@/lib/api/endpoints";
import { apiClient } from "@/lib/api/client";
import { queryKeys } from "@/lib/query/keys";
import { useAuthStore } from "@/stores/auth-store";
import { useOrganizationStore } from "@/stores/organization-store";
import type { User } from "@/types/auth";
import type { Organization } from "@/types/organization";

export function useAuthBootstrap() {
  const tokens = useAuthStore((state) => state.tokens);
  const setUser = useAuthStore((state) => state.setUser);
  const logout = useAuthStore((state) => state.logout);
  const markBootstrapped = useAuthStore((state) => state.markBootstrapped);
  const setAvailableOrganizations = useOrganizationStore((state) => state.setAvailableOrganizations);

  const enabled = Boolean(tokens?.access);

  const meQuery = useQuery({
    queryKey: queryKeys.me(),
    queryFn: async () => {
      const response = await apiClient.get<User>(endpoints.auth.me);
      return response.data;
    },
    enabled,
    retry: false,
  });

  const organizationsQuery = useQuery({
    queryKey: queryKeys.organizations(),
    queryFn: async () => {
      const response = await apiClient.get<Organization[]>(endpoints.organizations.list);
      return response.data;
    },
    enabled,
    retry: false,
  });

  useEffect(() => {
    if (!enabled) {
      setAvailableOrganizations([]);
      markBootstrapped();
      return;
    }

    if (meQuery.isSuccess) {
      setUser(meQuery.data);
    }

    if (organizationsQuery.isSuccess) {
      setAvailableOrganizations(organizationsQuery.data);
    }

    if (meQuery.isError || organizationsQuery.isError) {
      logout();
    }

    if (
      meQuery.status !== "pending" &&
      organizationsQuery.status !== "pending" &&
      (meQuery.isSuccess || meQuery.isError) &&
      (organizationsQuery.isSuccess || organizationsQuery.isError)
    ) {
      markBootstrapped();
    }
  }, [
    enabled,
    logout,
    markBootstrapped,
    meQuery.data,
    meQuery.isError,
    meQuery.isSuccess,
    meQuery.status,
    organizationsQuery.data,
    organizationsQuery.isError,
    organizationsQuery.isSuccess,
    organizationsQuery.status,
    setAvailableOrganizations,
    setUser,
  ]);
}
