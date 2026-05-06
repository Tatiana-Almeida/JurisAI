import type { OCRAuditLog } from "@/types/ocr";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type OCRAuditLogTableProps = {
  logs: OCRAuditLog[];
};

export function OCRAuditLogTable({ logs }: OCRAuditLogTableProps) {
  if (logs.length === 0) {
    return (
      <EmptyState
        title="Sem audit logs de OCR"
        description="Os logs de auditoria do OCR aparecem aqui quando houver execuções ou falhas."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Audit trail OCR</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {logs.slice(0, 6).map((log) => (
          <div key={log.id} className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">{log.action ?? "evento OCR"}</div>
            <div className="mt-1 text-muted-foreground">
              provider={log.provider ?? "local"} · status={log.status ?? "unknown"} · reason={log.reason ?? "n/a"}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
