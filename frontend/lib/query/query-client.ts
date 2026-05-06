import { QueryClient } from "@tanstack/react-query";
import { organizationScopedPrefixes } from "@/lib/query/keys";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      retry: (failureCount, error) => {
        const status = (error as { status?: number })?.status;
        if (status === 401 || status === 403 || status === 402) {
          return false;
        }
        return failureCount < 2;
      },
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});

export function clearTenantCache(client: QueryClient, organizationId?: string | null) {
  if (!organizationId) {
    return;
  }

  client.removeQueries({
    predicate: (query) =>
      Array.isArray(query.queryKey) &&
      query.queryKey.includes(organizationId) &&
      organizationScopedPrefixes.includes(
        String(query.queryKey[0]) as (typeof organizationScopedPrefixes)[number],
      ),
  });
}

export function invalidateOrganizationScopedQueries(
  client: QueryClient,
  organizationId?: string | null,
) {
  if (!organizationId) {
    return;
  }

  client.invalidateQueries({
    predicate: (query) =>
      Array.isArray(query.queryKey) &&
      query.queryKey.includes(organizationId) &&
      organizationScopedPrefixes.includes(
        String(query.queryKey[0]) as (typeof organizationScopedPrefixes)[number],
      ),
  });
}
