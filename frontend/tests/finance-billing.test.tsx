import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import FinancePage from "@/app/finance/page";
import BillingPage from "@/app/billing/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-finance", () => ({
  useFinanceSummary: () => ({
    data: { total_invoices: 0, open_invoices: 0, paid_invoices: 0, total_payments: 0, payments_amount: 0, expenses_amount: 0 },
    isLoading: false,
    isError: false,
  }),
  useFinanceInvoices: () => ({
    data: [],
    isLoading: false,
    isError: false,
  }),
  useFinanceExpenses: () => ({
    data: [],
    isLoading: false,
    isError: false,
  }),
}));

vi.mock("@/hooks/use-billing", () => ({
  useBillingSummary: () => ({
    data: {
      subscriptions: [],
      invoices: [],
    },
    isLoading: false,
    isError: false,
  }),
}));

describe("finance and billing pages", () => {
  it("renders honest partial finance state", () => {
    render(<FinancePage />);
    expect(screen.getByText("Financeiro em preparacao operacional")).toBeInTheDocument();
  });

  it("renders honest billing readiness state", () => {
    render(<BillingPage />);
    expect(screen.getByText("Billing integration pending")).toBeInTheDocument();
    expect(screen.getAllByText(/checkout pending/i).length).toBeGreaterThan(0);
  });
});
