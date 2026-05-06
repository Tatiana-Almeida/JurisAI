import { ModuleStateCard } from "@/components/shared/module-state-card";

export function OCRSettingsPanel() {
  return (
    <ModuleStateCard
      title="OCR settings"
      status="partial"
      description="Estrutura base para governança de OCR por organização."
      bullets={[
        "Limites por tenant serão configuráveis no MVP.",
        "Opt-in para modos locais e externos já está previsto.",
      ]}
    />
  );
}
