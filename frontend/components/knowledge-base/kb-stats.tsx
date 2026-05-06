import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type KBStatsProps = {
  stats?: Record<string, unknown>;
};

export function KBStats({ stats }: KBStatsProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Estado da base</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-3 text-sm text-muted-foreground md:grid-cols-2">
        <div>documentos: {String(stats?.total_documents ?? "—")}</div>
        <div>documentos indexados: {String(stats?.indexed_documents ?? "—")}</div>
        <div>documentos falhados: {String(stats?.failed_documents ?? "—")}</div>
        <div>consultas: {String(stats?.total_queries ?? "—")}</div>
      </CardContent>
    </Card>
  );
}
