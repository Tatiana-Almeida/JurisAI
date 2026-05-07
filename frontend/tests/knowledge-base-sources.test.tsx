import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SourcesList } from "@/components/knowledge-base/sources-list";

describe("knowledge base sources list", () => {
  it("shows retrieval scores and fallback metadata", () => {
    render(
      <SourcesList
        confidence={0.74}
        retrievalMethod="hybrid"
        fallbackUsed
        fallbackReason="semantic-disabled"
        sources={[
          {
            title: "Peca processual",
            excerpt: "Trecho relevante...",
            document_id: "doc-2",
            final_score: 0.88,
            text_score: 0.77,
            embedding_score: 0.66,
          },
        ]}
      />,
    );

    expect(screen.getByText("Peca processual")).toBeInTheDocument();
    expect(screen.getByText(/fallback_reason=semantic-disabled/)).toBeInTheDocument();
    expect(screen.getByText(/final_score=0.88/)).toBeInTheDocument();
  });
});
