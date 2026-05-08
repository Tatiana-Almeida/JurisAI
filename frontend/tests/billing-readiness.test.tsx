import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { BillingStatusCard } from "@/components/billing/billing-status-card";

describe("billing readiness", () => {
  it("keeps billing honest about pending commercial flows", () => {
    render(<BillingStatusCard subscriptions={[]} invoices={[]} />);

    expect(screen.getByText("Billing integration pending")).toBeInTheDocument();
    expect(screen.getByText(/Billing ainda esta em preparacao para cobranca real/)).toBeInTheDocument();
    expect(screen.getByText(/Checkout pending/)).toBeInTheDocument();
    expect(screen.getByText(/Subscription enforcement pending/)).toBeInTheDocument();
  });
});
