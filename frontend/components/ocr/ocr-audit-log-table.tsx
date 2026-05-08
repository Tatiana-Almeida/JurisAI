import type { OCRAuditLog } from "@/types/ocr";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type OCRAuditLogTableProps = {
  logs: OCRAuditLog[];
};

function previewMetadata(metadata?: Record<string, unknown>) {
  if (!metadata) {
    return "Sem metadata adicional.";
  }

  return JSON.stringify(metadata, null, 2);
}

export function OCRAuditLogTable({ logs }: OCRAuditLogTableProps) {
  if (logs.length === 0) {
    return (
      <EmptyState
        title="Sem audit logs de OCR"
        description="Os logs de auditoria de OCR aparecem aqui quando houver execucoes, falhas ou aplicacoes ao documento."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Audit trail OCR</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {logs.map((log) => (
          <div key={log.id} className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="font-medium">{log.action ?? "evento OCR"}</div>
              <div className="text-xs text-muted-foreground">{log.created_at ?? "sem data"}</div>
            </div>
            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-muted-foreground">
              <span>provider: {log.provider ?? "local"}</span>
              <span>status: {log.status ?? "desconhecido"}</span>
              <span>modo: {log.mode ?? "n/d"}</span>
              <span>documento: {log.document ?? "n/d"}</span>
            </div>
            {log.reason ? <p className="mt-2 text-amber-700 dark:text-amber-300">{log.reason}</p> : null}
            <pre className="mt-3 overflow-auto rounded-xl bg-muted/50 p-3 text-xs text-muted-foreground">
              {previewMetadata(log.metadata)}
            </pre>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
