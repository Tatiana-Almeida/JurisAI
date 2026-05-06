"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api/client";
import { endpoints } from "@/lib/api/endpoints";
import { queryKeys } from "@/lib/query/keys";
import type { Organization } from "@/types/organization";

export function useOrganizations(enabled = true) {
  return useQuery({
    queryKey: queryKeys.organizations(),
    queryFn: async () => {
      const response = await apiClient.get<Organization[]>(endpoints.organizations.list);
      return response.data;
    },
    enabled,
    retry: false,
  });
}
