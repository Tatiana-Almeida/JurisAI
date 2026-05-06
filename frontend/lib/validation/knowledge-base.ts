import { z } from "zod";

export const knowledgeBaseSchema = z.object({
  name: z.string().min(2, "O nome é obrigatório."),
  description: z.string().optional(),
});
