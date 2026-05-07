import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { OCRJobTable } from "@/components/ocr/ocr-job-table";
import { OCRResultCard } from "@/components/ocr/ocr-result-card";

describe("ocr flow UI", () => {
  it("shows polling state for running jobs", () => {
    render(
      <OCRJobTable
        jobs={[
          {
            id: "job-1",
            document: "doc-1",
            status: "running",
            extraction_method: "advanced_ocr",
            created_at: "2026-05-06T10:00:00Z",
          },
        ]}
      />,
    );

    expect(screen.getByText("Polling ativo")).toBeInTheDocument();
    expect(screen.getByText("advanced_ocr")).toBeInTheDocument();
  });

  it("applies OCR result through the provided callback", () => {
    const onApply = vi.fn();

    render(
      <OCRResultCard
        result={{
          id: "result-1",
          document_id: "doc-1",
          extracted_text: "Texto extraido.",
          char_count: 123,
          metadata: {
            confidence: 0.83,
            pages_processed: 5,
          },
        }}
        onApply={onApply}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Aplicar ao documento" }));
    expect(onApply).toHaveBeenCalledTimes(1);
  });
});
