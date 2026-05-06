import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import DashboardPage from "@/app/dashboard/page";

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganization: { id: "org-1", name: "JurisAI Demo" },
    activeOrganizationId: "org-1",
    availableOrganizations: [],
  }),
}));

vi.mock("@/hooks/use-jurisai-queries", () => ({
  useHealthStatus: () => ({ data: { status: "ok" } }),
  useDashboardSummary: () => ({
    data: {
      total_cases: 3,
      active_cases: 2,
      total_documents: 5,
      upcoming_deadlines: 1,
      overdue_deadlines: 0,
      pending_tasks: 1,
      completed_tasks: 0,
      pending_invoices: 2,
    },
    isLoading: false,
    isError: false,
  }),
  useDashboardDeadlines: () => ({ data: [], isLoading: false, isError: false }),
  useDashboardDocuments: () => ({ data: [], isLoading: false, isError: false }),
  useDashboardFinancial: () => ({ data: { paid_invoices: 1 }, isLoading: false, isError: false }),
  useCases: () => ({ data: [], isLoading: false, isError: false }),
  useOCRJobs: () => ({ data: [], isLoading: false, isError: false }),
}));

describe("dashboard page", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("renders the dashboard heading and metrics", () => {
    render(<DashboardPage />);
    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Dashboard",
      }),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Processos").length).toBeGreaterThan(0);
    expect(screen.getByText("Estado do sistema")).toBeInTheDocument();
  });
});
