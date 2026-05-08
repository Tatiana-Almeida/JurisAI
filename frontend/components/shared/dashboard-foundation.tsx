import { ModuleStateCard } from "@/components/shared/module-state-card";

export function DashboardFoundation() {
  return (
    <div className="grid gap-4 xl:grid-cols-3">
      <ModuleStateCard
        title="Backend foundation"
        status="active"
        description="Os endpoints de dashboard, processos, documentos e OCR já existem no backend."
        bullets={[
          "O frontend agora está pronto para consumi-los com React Query.",
          "Multi-tenancy foi preparada desde a base.",
        ]}
      />
      <ModuleStateCard
        title="Billing honesty"
        status="partial"
        description="Billing seguirá fiel ao estado real do backend."
        bullets={[
          "Sem checkout ativo por enquanto.",
          "Subscription status será tratado como leitura, não como venda fechada.",
        ]}
      />
      <ModuleStateCard
        title="AI readiness"
        status="partial"
        description="A UI de IA nasce com fontes, estados e limites claros."
        bullets={[
          "Sem vender mocks como produto final.",
          "RAG e OCR terão estados explícitos de active/partial/pending.",
        ]}
      />
    </div>
  );
}
