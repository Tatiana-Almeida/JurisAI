import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import DocumentDetailPage from "@/app/documents/[id]/page";

const pushMock = vi.fn();
const runOCRMock = vi.fn();
const runAdvancedOCRMock = vi.fn();

vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "doc-1" }),
  useRouter: () => ({ push: pushMock }),
}));

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
  }),
}));

vi.mock("@/hooks/use-documents", () => ({
  useDocument: () => ({
    data: {
      id: "doc-1",
      type: "petition",
      content: "Conteúdo",
      version: 1,
      law_case_id: "case-1",
    },
    isLoading: false,
    isError: false,
  }),
}));

vi.mock("@/hooks/use-ocr", () => ({
  useRunOCR: () => ({
    isPending: false,
    mutateAsync: runOCRMock,
  }),
  useRunAdvancedOCR: () => ({
    isPending: false,
    mutateAsync: runAdvancedOCRMock,
  }),
}));

describe("document OCR actions", () => {
  it("calls the correct OCR endpoints via hooks", async () => {
    runOCRMock.mockResolvedValueOnce({});
    runAdvancedOCRMock.mockResolvedValueOnce({});
    render(<DocumentDetailPage />);

    fireEvent.click(screen.getByRole("button", { name: "Executar OCR" }));
    await waitFor(() => expect(runOCRMock).toHaveBeenCalledWith("doc-1"));

    fireEvent.click(screen.getByRole("button", { name: "Executar OCR avançado" }));
    await waitFor(() => expect(runAdvancedOCRMock).toHaveBeenCalledWith("doc-1"));
  });
});
