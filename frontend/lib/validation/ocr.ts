import { z } from "zod";

export const ocrSettingsSchema = z.object({
  advanced_ocr_enabled: z.boolean(),
  external_ocr_enabled: z.boolean(),
  allow_document_content_to_external_ocr_provider: z.boolean(),
  preferred_ocr_provider: z.string().min(1, "Selecione um provider."),
  preferred_ocr_model: z.string().optional(),
  image_ocr_mode: z.string().min(1, "Selecione o modo de OCR de imagem."),
  scanned_pdf_ocr_mode: z.string().min(1, "Selecione o modo de OCR para PDF digitalizado."),
  max_scanned_pdf_pages: z.number().int().min(1).max(500),
  max_ocr_file_size_mb: z.number().int().min(1).max(2048),
  max_ocr_chars_output: z.number().int().min(100).max(1_000_000),
  store_page_level_ocr: z.boolean(),
  require_human_review: z.boolean(),
});

export const ocrKnowledgeBasePipelineSchema = z.object({
  document_id: z.string().min(1, "Selecione um documento."),
  knowledge_base_id: z.string().min(1, "Selecione uma Knowledge Base."),
  update_document_content: z
    .boolean()
    .refine((value) => value === true, "Confirme explicitamente a atualizacao de Document.content para este fluxo."),
});
