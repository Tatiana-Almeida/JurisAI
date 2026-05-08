import type { Document } from "@/types/documents";
import type { LawCase } from "@/types/cases";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ModuleStateCard } from "@/components/shared/module-state-card";

type ClientPortalHomeProps = {
  cases: LawCase[];
  documents: Document[];
  messagesCount?: number;
};

export function ClientPortalHome({
  cases,
  documents,
  messagesCount = 0,
}: ClientPortalHomeProps) {
  return (
    <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
      <Card className="jurisai-panel rounded-3xl">
        <CardHeader>
          <CardTitle>Portal do Cliente</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-muted-foreground">
          <div>Processos partilhados: {cases.length}</div>
          <div>Documentos partilhados: {documents.length}</div>
          <div>Mensagens acessiveis: {messagesCount}</div>
          <div>
            Este portal continua em fundacao e depende da curadoria de shares, visibilidade e mensagens do backend.
          </div>
        </CardContent>
      </Card>
      <ModuleStateCard
        title="Portal foundation"
        status="partial"
        description="O backend ja expoe casos, documentos e mensagens do portal, mas a experiencia final do cliente ainda sera refinada no MVP."
        bullets={[
          "Sem prometer onboarding final nesta fase.",
          "Sem fingir experiencia publica pronta para venda.",
          "Dados continuam isolados pela organizacao autenticada.",
        ]}
      />
    </div>
  );
}
