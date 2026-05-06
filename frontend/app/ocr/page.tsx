import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { OCRAuditLogTable } from "@/components/ocr/ocr-audit-log-table";
import { OCRJobTable } from "@/components/ocr/ocr-job-table";
import { OCRResultCard } from "@/components/ocr/ocr-result-card";
import { OCRSettingsPanel } from "@/components/ocr/ocr-settings-panel";
import { PageResultsTable } from "@/components/ocr/page-results-table";

export default function OCRPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="OCR"
          description="A fundação de OCR do frontend já considera jobs, resultados, page results, auditoria e settings por tenant."
        />
        <div className="grid gap-4 xl:grid-cols-2">
          <OCRJobTable />
          <OCRResultCard />
          <OCRSettingsPanel />
          <OCRAuditLogTable />
          <PageResultsTable />
        </div>
      </div>
    </AppShell>
  );
}
