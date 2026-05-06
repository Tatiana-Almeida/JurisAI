import { render, screen } from "@testing-library/react";
import DashboardPage from "@/app/dashboard/page";

describe("dashboard page", () => {
  it("renders the dashboard foundation heading", () => {
    render(<DashboardPage />);
    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Dashboard",
      }),
    ).toBeInTheDocument();
    expect(screen.getByText("Backend foundation")).toBeInTheDocument();
  });
});
