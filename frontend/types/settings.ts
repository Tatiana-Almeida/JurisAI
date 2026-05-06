import type { OCRSettings } from "@/types/ocr";
import type { RAGSettings } from "@/types/knowledge-base";

export interface AppSettings {
  ocr?: OCRSettings;
  rag?: RAGSettings;
  theme?: "light" | "dark" | "system";
}
