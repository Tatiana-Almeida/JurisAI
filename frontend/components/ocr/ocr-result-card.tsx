import { ModuleStateCard } from "@/components/shared/module-state-card";

export function OCRResultCard() {
  return (
    <ModuleStateCard
      title="OCR results"
      status="partial"
      description="Preparado para mostrar texto extraído, status e metadados do backend."
      bullets={[
        "Suporte a empty/loading/error state preparado.",
        "Conexão com OCRResult entra na próxima fase.",
      ]}
    />
  );
}
