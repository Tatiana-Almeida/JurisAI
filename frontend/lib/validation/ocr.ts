import { z } from "zod";

export const ocrSettingsSchema = z.object({
  maxScannedPdfPages: z.number().min(1).max(200).optional(),
  maxOcrFileSizeMb: z.number().min(1).max(100).optional(),
});
