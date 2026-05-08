import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { IndexingJobsTable } from "@/components/knowledge-base/indexing-jobs-table";

describe("indexing jobs table", () => {
  it("renders indexing job rows with links", () => {
    render(
      <IndexingJobsTable
        jobs={[
          {
            id: "job-1",
            status: "running",
            document: "doc-1",
            knowledge_base: "kb-1",
            chunks_created: 4,
            chunks_deleted: 0,
          },
        ]}
      />,
    );

    expect(screen.getByText("running")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Documento" })).toHaveAttribute(
      "href",
      "/documents/doc-1",
    );
    expect(screen.getByRole("link", { name: "Base" })).toHaveAttribute(
      "href",
      "/knowledge-base/kb-1",
    );
  });
});
