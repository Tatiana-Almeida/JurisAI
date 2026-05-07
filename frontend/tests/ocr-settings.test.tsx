import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { OCRSettingsPanel } from "@/components/ocr/ocr-settings-panel";

const mutateAsyncMock = vi.fn();

vi.mock("@/hooks/use-ocr", () => ({
  useUpdateOCRSettings: () => ({
    mutateAsync: mutateAsyncMock,
    isPending: false,
  }),
}));

describe("ocr settings panel", () => {
  it("maps DRF errors returned by the settings endpoint", async () => {
    mutateAsyncMock.mockRejectedValueOnce({
      response: {
        data: {
          preferred_ocr_provider: ["Provider invalido."],
        },
      },
    });

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

    fireEvent.click(screen.getByRole("button", { name: "Guardar configuracoes" }));

    await waitFor(() => {
      expect(screen.getByText("Provider invalido.")).toBeInTheDocument();
    });
  });
});
