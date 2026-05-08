import Link from "next/link";
import type { KnowledgeBase } from "@/types/knowledge-base";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type KBListProps = {
  knowledgeBases: KnowledgeBase[];
};

export function KBList({ knowledgeBases }: KBListProps) {
  if (knowledgeBases.length === 0) {
    return (
      <EmptyState
        title="Sem Knowledge Bases"
        description="Crie a primeira base apenas se este módulo já fizer sentido para a operação atual."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Bases de conhecimento</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {knowledgeBases.map((knowledgeBase) => (
          <Link
            key={knowledgeBase.id}
            href={`/knowledge-base/${knowledgeBase.id}`}
            className="block rounded-2xl border border-border/60 p-4 transition-colors hover:border-primary/40 hover:bg-primary/5"
          >
            <div className="font-medium">{knowledgeBase.name}</div>
            <div className="mt-1 text-sm text-muted-foreground">
              {knowledgeBase.description || "Sem descrição"} · ativa={String(knowledgeBase.is_active ?? true)}
            </div>
          </Link>
        ))}
      </CardContent>
    </Card>
  );
}
