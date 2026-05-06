import type { Document } from "@/types/documents";
import type { LawCase } from "@/types/cases";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ModuleStateCard } from "@/components/shared/module-state-card";

type ClientPortalHomeProps = {
  cases: LawCase[];
  documents: Document[];
};

export function ClientPortalHome({ cases, documents }: ClientPortalHomeProps) {
  return (
    <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
      <Card className="jurisai-panel rounded-3xl">
        <CardHeader>
          <CardTitle>Portal do Cliente</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-muted-foreground">
          <div>Processos partilhados: {cases.length}</div>
          <div>Documentos partilhados: {documents.length}</div>
          <div>Este portal continua em fundação e depende da curadoria de shares e visibilidade no backend.</div>
        </CardContent>
      </Card>
      <ModuleStateCard
        title="Portal foundation"
        status="partial"
        description="O backend já expõe casos, documentos e mensagens do portal, mas a experiência final do cliente ainda será refinada no MVP."
        bullets={[
          "Sem prometer onboarding final nesta fase.",
          "Sem fingir experiência pública pronta para venda.",
        ]}
      />
    </div>
  );
}
