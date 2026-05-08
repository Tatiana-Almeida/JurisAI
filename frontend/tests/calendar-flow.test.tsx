import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import CalendarPage from "@/app/calendar/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-calendar", () => ({
  useCalendarEvents: () => ({
    data: [],
    isLoading: false,
    isError: false,
  }),
}));

describe("calendar page", () => {
  it("renders empty calendar state", () => {
    render(<CalendarPage />);

    expect(screen.getByRole("heading", { name: "Calendario" })).toBeInTheDocument();
    expect(screen.getByText("Sem eventos")).toBeInTheDocument();
  });
});
