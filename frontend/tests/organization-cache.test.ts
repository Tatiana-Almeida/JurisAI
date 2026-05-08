import { QueryClient } from "@tanstack/react-query";
import { beforeEach, describe, expect, it } from "vitest";
import { clearTenantCache } from "@/lib/query/query-client";
import { queryKeys } from "@/lib/query/keys";
import { useOrganizationStore } from "@/stores/organization-store";

describe("organization cache isolation", () => {
  beforeEach(() => {
    useOrganizationStore.setState({
      activeOrganizationId: null,
      availableOrganizations: [],
      loadStatus: "idle",
      loadError: null,
    });
  });

  it("clears only organization scoped cache for the previous tenant", () => {
    const client = new QueryClient();
    client.setQueryData(queryKeys.cases("org-a"), [{ id: "1" }]);
    client.setQueryData(queryKeys.cases("org-b"), [{ id: "2" }]);

    clearTenantCache(client, "org-a");

    expect(client.getQueryData(queryKeys.cases("org-a"))).toBeUndefined();
    expect(client.getQueryData(queryKeys.cases("org-b"))).toEqual([{ id: "2" }]);
  });

  it("builds organization-scoped keys and auto-selects the only organization", () => {
    useOrganizationStore.getState().bootstrapOrganizations([
      { id: "org-1", name: "Org 1" },
    ]);

    expect(useOrganizationStore.getState().activeOrganizationId).toBe("org-1");
    expect(useOrganizationStore.getState().loadStatus).toBe("ready");
    expect(queryKeys.cases("org-1")[1]).toBe("org-1");
    expect(queryKeys.documents("org-1")[1]).toBe("org-1");
    expect(queryKeys.billing("org-1")[1]).toBe("org-1");
  });

  it("stores a friendly load error when organizations fail to load", () => {
    useOrganizationStore.getState().setLoadError("Falha de staging.");

    expect(useOrganizationStore.getState().loadStatus).toBe("error");
    expect(useOrganizationStore.getState().loadError).toBe("Falha de staging.");
    expect(useOrganizationStore.getState().activeOrganizationId).toBeNull();
  });
});
