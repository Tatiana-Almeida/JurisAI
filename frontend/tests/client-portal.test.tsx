import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ClientPortalPage from "@/app/client-portal/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-jurisai-queries", () => ({
  useClientPortalData: () => ({
    data: {
      cases: [],
      documents: [],
      messages: [],
    },
    isLoading: false,
    isError: false,
  }),
}));

describe("client portal page", () => {
  it("renders the client portal foundation state", () => {
    render(<ClientPortalPage />);

    expect(screen.getByRole("heading", { name: "Portal do Cliente" })).toBeInTheDocument();
    expect(screen.getByText("Portal foundation")).toBeInTheDocument();
  });
});
