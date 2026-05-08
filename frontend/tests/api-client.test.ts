import { describe, expect, it } from "vitest";
import { buildAuthHeader, getApiBaseUrl } from "@/lib/api/client";

describe("api client foundation", () => {
  it("builds auth header safely", () => {
    expect(buildAuthHeader("abc")).toEqual({ Authorization: "Bearer abc" });
    expect(buildAuthHeader(null)).toEqual({});
  });

  it("resolves an API base url", () => {
    expect(getApiBaseUrl()).toBeTruthy();
  });
});
