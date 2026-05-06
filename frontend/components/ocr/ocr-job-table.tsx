import { ModuleStateCard } from "@/components/shared/module-state-card";

export function OCRJobTable() {
  return (
    <ModuleStateCard
      title="OCR jobs"
      status="partial"
      description="Foundation pronta para listar jobs com estados pending, running, completed, failed e skipped."
      bullets={[
        "Tabela ainda não ligada ao endpoint real.",
        "Estados operacionais já modelados para UI.",
      ]}
    />
  );
}
