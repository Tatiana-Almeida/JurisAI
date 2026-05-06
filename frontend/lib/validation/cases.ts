import { z } from "zod";

export const caseSchema = z.object({
  title: z.string().min(3, "O título é obrigatório."),
  description: z.string().optional(),
  status: z.string().optional(),
});
