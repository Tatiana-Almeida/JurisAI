import Link from "next/link";
import type { LawCase } from "@/types/cases";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type RecentCasesProps = {
  cases: LawCase[];
};

export function RecentCases({ cases }: RecentCasesProps) {
  if (cases.length === 0) {
    return (
      <EmptyState
        title="Sem processos recentes"
        description="Os processos desta organização vão aparecer aqui assim que existirem dados."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Processos recentes</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {cases.slice(0, 5).map((lawCase) => (
          <Link
            key={lawCase.id}
            href={`/cases/${lawCase.id}`}
            className="block rounded-2xl border border-border/60 p-4 transition-colors hover:border-primary/40 hover:bg-primary/5"
          >
            <div className="font-medium">{lawCase.title}</div>
            <div className="mt-1 text-sm text-muted-foreground">
              Cliente: {lawCase.client?.name ?? "Por validar"} · Estado: {lawCase.status ?? "open"}
            </div>
          </Link>
        ))}
      </CardContent>
    </Card>
  );
}
