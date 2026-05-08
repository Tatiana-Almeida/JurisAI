import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import DeadlinesPage from "@/app/deadlines/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-deadlines", () => ({
  useDeadlines: () => ({
    data: [],
    isLoading: false,
    isError: false,
  }),
}));

describe("deadlines page", () => {
  it("renders empty state and filters safely", () => {
    render(<DeadlinesPage />);

    expect(screen.getByRole("heading", { name: "Prazos" })).toBeInTheDocument();
    expect(screen.getByText("Sem prazos")).toBeInTheDocument();
    expect(screen.getByDisplayValue("30")).toBeInTheDocument();
  });
});
