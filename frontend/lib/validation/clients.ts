import { z } from "zod";

export const clientSchema = z.object({
  name: z.string().min(2, "O nome é obrigatório."),
  email: z.email("Introduza um email válido."),
  password: z.string().min(8, "A password inicial deve ter pelo menos 8 caracteres."),
});
