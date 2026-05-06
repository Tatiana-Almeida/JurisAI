import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ClientsPage from "@/app/clients/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-clients", () => ({
  useClients: () => ({
    data: [],
    isLoading: false,
    isError: false,
  }),
  useCreateClient: () => ({
    isPending: false,
    mutateAsync: vi.fn(),
  }),
}));

describe("clients page", () => {
  it("renders empty state when there are no clients", () => {
    render(<ClientsPage />);
    expect(screen.getByText("Sem clientes")).toBeInTheDocument();
  });
});
