import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { CaseForm } from "@/components/cases/case-form";

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-jurisai-queries", () => ({
  useCreateCase: () => ({
    isPending: false,
    mutateAsync: vi.fn(),
  }),
  useClients: () => ({
    data: [{ id: "client-1", name: "Cliente A" }],
    isLoading: false,
  }),
  useLawyers: () => ({
    data: [{ id: "lawyer-1", name: "Advogado A", email: "a@example.com" }],
    isLoading: false,
  }),
}));

describe("case form", () => {
  it("validates required fields", async () => {
    render(<CaseForm />);

    fireEvent.click(screen.getByRole("button", { name: "Criar processo" }));

    expect(await screen.findByText("O título é obrigatório.")).toBeInTheDocument();
    expect(await screen.findByText("Selecione um cliente.")).toBeInTheDocument();
    expect(await screen.findByText("Selecione um advogado.")).toBeInTheDocument();
  });
});
