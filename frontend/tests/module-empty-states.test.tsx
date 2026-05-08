import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ClientsPage from "@/app/clients/page";
import CasesPage from "@/app/cases/page";
import DocumentsPage from "@/app/documents/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: null,
    activeOrganization: null,
  }),
}));

vi.mock("@/hooks/use-clients", () => ({
  useClients: () => ({ data: [], isLoading: false, isError: false }),
  useCreateClient: () => ({ mutateAsync: vi.fn(), isPending: false }),
}));

vi.mock("@/hooks/use-cases", () => ({
  useCases: () => ({ data: [], isLoading: false, isError: false }),
}));

vi.mock("@/hooks/use-documents", () => ({
  useDocuments: () => ({ data: [], isLoading: false, isError: false }),
  useUploadDocument: () => ({ mutateAsync: vi.fn(), isPending: false }),
}));

describe("module empty states without tenant", () => {
  it("guides the user to select an organization in clients, cases and documents", () => {
    render(
      <>
        <ClientsPage />
        <CasesPage />
        <DocumentsPage />
      </>,
    );

    expect(screen.getAllByText("Selecione uma organizacao").length).toBeGreaterThanOrEqual(3);
  });
});
