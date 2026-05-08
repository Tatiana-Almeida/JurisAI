import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import SettingsPage from "@/app/settings/page";

vi.mock("@/components/layout/app-shell", () => ({
  AppShell: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganizationId: "org-1",
    activeOrganization: { id: "org-1", name: "Org Demo", plan: "growth" },
  }),
}));

vi.mock("@/stores/auth-store", () => ({
  useAuthStore: (selector: (state: { user: { email: string; role: string } }) => unknown) =>
    selector({
      user: { email: "advogado@example.com", role: "advogado" },
    }),
}));

vi.mock("@/hooks/use-jurisai-queries", () => ({
  useOCRSettings: () => ({
    data: {
      preferred_ocr_provider: "local",
      image_ocr_mode: "auto",
      scanned_pdf_ocr_mode: "auto",
      max_scanned_pdf_pages: 50,
      max_ocr_file_size_mb: 25,
      max_ocr_chars_output: 120000,
    },
    isLoading: false,
    isError: false,
  }),
  useRAGSettings: () => ({
    data: {
      retrieval_mode: "hybrid",
      embedding_provider: "local",
      embedding_model: "local-hash-v1",
      external_embeddings_enabled: false,
      require_human_review_for_ai_answers: true,
      allow_document_content_to_external_provider: false,
      max_sources_per_answer: 5,
      min_confidence_threshold: "0.30",
    },
    isLoading: false,
    isError: false,
  }),
}));

vi.mock("@/hooks/use-ocr", () => ({
  useUpdateOCRSettings: () => ({ mutateAsync: vi.fn(), isPending: false }),
}));

vi.mock("@/hooks/use-knowledge-base", () => ({
  useUpdateRAGSettings: () => ({ mutateAsync: vi.fn(), isPending: false }),
}));

describe("settings page", () => {
  it("renders operational settings cards", () => {
    render(<SettingsPage />);

    expect(screen.getByRole("heading", { name: "Configuracoes" })).toBeInTheDocument();
    expect(screen.getByText("Conta")).toBeInTheDocument();
    expect(screen.getByText("Organizacao ativa")).toBeInTheDocument();
    expect(screen.getByText("Configuracoes de OCR")).toBeInTheDocument();
  });
});
