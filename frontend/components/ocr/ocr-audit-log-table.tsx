import { ModuleStateCard } from "@/components/shared/module-state-card";

export function OCRAuditLogTable() {
  return (
    <ModuleStateCard
      title="OCR audit logs"
      status="partial"
      description="UI base preparada para observabilidade e auditoria do pipeline OCR."
      bullets={[
        "Provider, mode, reason e status terão tabela dedicada.",
        "Ainda sem ligação ao endpoint real.",
      ]}
    />
  );
}
