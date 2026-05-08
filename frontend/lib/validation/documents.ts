import { z } from "zod";

export const allowedDocumentExtensions = [
  "pdf",
  "docx",
  "txt",
  "png",
  "jpg",
  "jpeg",
] as const;

export const documentSchema = z.object({
  law_case_id: z.string().min(1, "Selecione um processo."),
  type: z.enum(["petition", "contract", "evidence", "internal"]),
  content: z.string().optional(),
});
