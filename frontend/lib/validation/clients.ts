import { z } from "zod";

export const clientSchema = z.object({
  name: z.string().min(2, "O nome é obrigatório."),
  email: z.email("Introduza um email válido.").optional().or(z.literal("")),
});
