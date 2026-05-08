import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { KBAsk } from "@/components/knowledge-base/kb-ask";

vi.mock("@/hooks/use-knowledge-base", () => ({
  useAskKnowledgeBase: () => ({
    isPending: false,
    mutateAsync: vi.fn(),
    data: {
      answer: "Resposta com evidencias fracas.",
      confidence: 0.12,
      retrieval_method: "local-hash-v1",
      effective_retrieval_mode: "local-hash-v1",
      fallback_used: true,
      fallback_reason: "textual_only",
      sources_count: 0,
      sources: [],
    },
  }),
}));

describe("knowledge base warnings", () => {
  it("shows low-confidence, no-sources, fallback and local-hash warnings", () => {
    render(<KBAsk knowledgeBaseId="kb-1" />);

    expect(screen.getByText(/Confianca baixa/)).toBeInTheDocument();
    expect(screen.getByText(/nao encontrou fontes suficientes/)).toBeInTheDocument();
    expect(screen.getByText(/Fallback textual utilizado/)).toBeInTheDocument();
    expect(screen.getByText(/local-hash-v1 valida o pipeline local/)).toBeInTheDocument();
  });
});
