import { beforeEach, describe, expect, it } from "vitest";
import { queryClient } from "@/lib/query/query-client";
import { queryKeys } from "@/lib/query/keys";
import { useAuthStore } from "@/stores/auth-store";
import { useOrganizationStore } from "@/stores/organization-store";

describe("auth store", () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.cookie =
      "jurisai-has-session=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    queryClient.clear();
    useOrganizationStore.setState({
      activeOrganizationId: "org-1",
      availableOrganizations: [{ id: "org-1", name: "Org 1" }],
    });
    useAuthStore.setState({
      status: "idle",
      user: null,
      tokens: null,
      isBootstrapped: false,
    });
  });

  it("bootstraps to unauthenticated when there is no token", () => {
    useAuthStore.getState().bootstrapAuth();
    expect(useAuthStore.getState().status).toBe("unauthenticated");
    expect(useAuthStore.getState().isBootstrapped).toBe(false);
  });

  it("logout clears tokens, auth state and tenant context", () => {
    queryClient.setQueryData(queryKeys.cases("org-1"), [{ id: "case-1" }]);
    useAuthStore.getState().setAuthenticated({
      user: { email: "advogado@example.com", role: "advogado" },
      tokens: { access: "access", refresh: "refresh" },
    });

    useAuthStore.getState().logout();

    expect(useAuthStore.getState().status).toBe("unauthenticated");
    expect(useAuthStore.getState().tokens).toBeNull();
    expect(useOrganizationStore.getState().activeOrganizationId).toBeNull();
    expect(queryClient.getQueryData(queryKeys.cases("org-1"))).toBeUndefined();
    expect(window.localStorage.getItem("jurisai.access-token")).toBeNull();
  });
});
