import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { KBAsk } from "@/components/knowledge-base/kb-ask";

vi.mock("@/hooks/use-knowledge-base", () => ({
  useAskKnowledgeBase: () => ({
    isPending: false,
    mutateAsync: vi.fn(),
    data: {
      answer: "Resposta juridica sintetizada.",
      confidence: 0.62,
      retrieval_method: "hybrid-local-hash-v1",
      fallback_used: false,
      sources: [
        {
          title: "Contrato de arrendamento",
          excerpt: "Clausula 4...",
          document_id: "doc-1",
          final_score: 0.91,
        },
      ],
    },
  }),
}));

describe("knowledge base ask", () => {
  it("renders answer, confidence and sources", () => {
    render(<KBAsk knowledgeBaseId="kb-1" />);

    expect(screen.getByText("Resposta juridica sintetizada.")).toBeInTheDocument();
    expect(screen.getAllByText(/confidence=0.62/).length).toBeGreaterThan(0);
    expect(screen.getByText("Contrato de arrendamento")).toBeInTheDocument();
  });
});
