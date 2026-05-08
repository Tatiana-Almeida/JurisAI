"use client";

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { endpoints } from "@/lib/api/endpoints";
import { apiClient } from "@/lib/api/client";
import { queryKeys } from "@/lib/query/keys";
import { useAuthStore } from "@/stores/auth-store";
import { useOrganizationStore } from "@/stores/organization-store";
import type { ApiError } from "@/types/api";
import type { User } from "@/types/auth";
import type { Organization } from "@/types/organization";

export function useAuthBootstrap() {
  const tokens = useAuthStore((state) => state.tokens);
  const bootstrapAuth = useAuthStore((state) => state.bootstrapAuth);
  const setUser = useAuthStore((state) => state.setUser);
  const setTokens = useAuthStore((state) => state.setTokens);
  const logout = useAuthStore((state) => state.logout);
  const markBootstrapped = useAuthStore((state) => state.markBootstrapped);
  const bootstrapOrganizations = useOrganizationStore((state) => state.bootstrapOrganizations);
  const setOrganizationsLoading = useOrganizationStore((state) => state.setLoading);
  const setOrganizationsLoadError = useOrganizationStore((state) => state.setLoadError);
  const clearOrganizationsLoadError = useOrganizationStore((state) => state.clearLoadError);
  const resetOrganizations = useOrganizationStore((state) => state.reset);

  const enabled = Boolean(tokens?.access);

  useEffect(() => {
    bootstrapAuth();
  }, [bootstrapAuth]);

  useEffect(() => {
    if (enabled) {
      setOrganizationsLoading();
    }
  }, [enabled, setOrganizationsLoading]);

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
    const meSettled = meQuery.status === "success" || meQuery.status === "error";
    const organizationsSettled =
      organizationsQuery.status === "success" || organizationsQuery.status === "error";

    if (!enabled) {
      setTokens(null);
      resetOrganizations();
      markBootstrapped();
      return;
    }

    if (meQuery.isSuccess) {
      setUser(meQuery.data);
    }

    if (organizationsQuery.isSuccess) {
      clearOrganizationsLoadError();
      bootstrapOrganizations(organizationsQuery.data);
    }

    if (meQuery.isError) {
      resetOrganizations();
      logout();
      return;
    }

    if (organizationsQuery.isError) {
      const status = (organizationsQuery.error as unknown as ApiError | undefined)?.status;

      if (status === 401 || status === 403) {
        resetOrganizations();
        logout();
        return;
      }

      setOrganizationsLoadError(
        "Nao foi possivel carregar as organizacoes deste utilizador. Verifique staging, rede ou permissoes.",
      );
    }

    if (meSettled && organizationsSettled) {
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
    organizationsQuery.error,
    organizationsQuery.isError,
    organizationsQuery.isSuccess,
    organizationsQuery.status,
    bootstrapOrganizations,
    clearOrganizationsLoadError,
    resetOrganizations,
    setOrganizationsLoadError,
    setTokens,
    setUser,
  ]);
}
