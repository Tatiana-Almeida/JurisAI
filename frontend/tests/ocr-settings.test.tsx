import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { OCRSettingsPanel } from "@/components/ocr/ocr-settings-panel";

vi.mock("@/hooks/use-ocr", () => ({
  useUpdateOCRSettings: () => ({
    mutateAsync: vi.fn(),
    isPending: false,
  }),
}));

describe("ocr settings panel", () => {
  it("renders operational OCR governance controls", () => {
    render(
      <OCRSettingsPanel
        settings={{
          preferred_ocr_provider: "local",
          image_ocr_mode: "auto",
          scanned_pdf_ocr_mode: "auto",
          max_scanned_pdf_pages: 50,
          max_ocr_file_size_mb: 25,
          max_ocr_chars_output: 120000,
        }}
      />,
    );

    expect(screen.getByText("Configuracoes de OCR")).toBeInTheDocument();
    expect(screen.getByText(/OCR externo continua desativado por padrao/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Guardar configuracoes" })).toBeInTheDocument();
  });
});
