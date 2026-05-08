import { z } from "zod";

export const caseSchema = z.object({
  title: z.string().min(3, "O título é obrigatório."),
  description: z.string().optional(),
  status: z.enum(["open", "in_progress", "closed", "on_hold"]),
  client_id: z.string().min(1, "Selecione um cliente."),
  lawyer_id: z.string().min(1, "Selecione um advogado."),
});

export const caseUpdateSchema = z.object({
  title: z.string().min(3, "O título é obrigatório."),
  description: z.string().optional(),
  status: z.enum(["open", "in_progress", "closed", "on_hold"]),
});
