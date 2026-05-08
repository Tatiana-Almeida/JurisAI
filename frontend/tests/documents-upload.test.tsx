import { fireEvent, render, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { DocumentUploadDropzone } from "@/components/documents/document-upload-dropzone";

describe("documents upload", () => {
  it("rejects invalid file extensions", async () => {
    const { container, findByText } = render(<DocumentUploadDropzone />);
    const input = container.querySelector("input");

    expect(input).not.toBeNull();

    fireEvent.change(input!, {
      target: {
        files: [new File(["content"], "malware.exe", { type: "application/octet-stream" })],
      },
    });

    await waitFor(async () => {
      expect(await findByText(/não foi possível aceitar o ficheiro|file type must be/i)).toBeInTheDocument();
    });
  });
});
