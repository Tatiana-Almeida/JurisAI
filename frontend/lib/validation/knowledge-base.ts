import { z } from "zod";

export const knowledgeBaseSchema = z.object({
  name: z.string().min(2, "O nome e obrigatorio."),
  description: z.string().max(1_000, "A descricao deve ter no maximo 1000 caracteres.").optional(),
});

export const knowledgeBaseSearchSchema = z.object({
  query: z.string().min(2, "Digite uma consulta com pelo menos 2 caracteres."),
});

export const ragSettingsSchema = z.object({
  retrieval_mode: z.string().min(1, "Selecione o modo de retrieval."),
  external_embeddings_enabled: z.boolean(),
  embedding_provider: z.string().min(1, "Selecione um provider."),
  embedding_model: z.string().optional(),
  require_human_review_for_ai_answers: z.boolean(),
  allow_document_content_to_external_provider: z.boolean(),
  max_sources_per_answer: z.number().int().min(1).max(20),
  min_confidence_threshold: z.string().min(1, "Indique um threshold minimo."),
});

export const prepareEmbeddingsSchema = z.object({
  knowledge_document_id: z.string().optional(),
});
