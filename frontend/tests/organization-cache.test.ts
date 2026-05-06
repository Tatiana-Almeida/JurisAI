import { QueryClient } from "@tanstack/react-query";
import { describe, expect, it } from "vitest";
import { clearTenantCache } from "@/lib/query/query-client";
import { queryKeys } from "@/lib/query/keys";

describe("organization cache isolation", () => {
  it("clears only organization scoped cache for the previous tenant", () => {
    const client = new QueryClient();
    client.setQueryData(queryKeys.cases("org-a"), [{ id: "1" }]);
    client.setQueryData(queryKeys.cases("org-b"), [{ id: "2" }]);

    clearTenantCache(client, "org-a");

    expect(client.getQueryData(queryKeys.cases("org-a"))).toBeUndefined();
    expect(client.getQueryData(queryKeys.cases("org-b"))).toEqual([{ id: "2" }]);
  });
});
