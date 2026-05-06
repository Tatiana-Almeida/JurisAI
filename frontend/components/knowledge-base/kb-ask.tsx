import { ModuleStateCard } from "@/components/shared/module-state-card";

export function KBAsk() {
  return (
    <ModuleStateCard
      title="KB ask"
      status="active"
      description="Foundation pronta para perguntas com fontes, fallback e explicabilidade."
      bullets={[
        "UI preparada para retrieval_method, confidence e fallback_reason.",
        "Sem provider externo obrigatório na fase inicial.",
      ]}
    />
  );
}
