"use client";

import { useParams } from "next/navigation";
import { toast } from "sonner";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { DocumentDetail } from "@/components/documents/document-detail";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useDocument, useRunOCR } from "@/hooks/use-jurisai-queries";

export default function DocumentDetailPage() {
  const params = useParams<{ id: string }>();
  const documentQuery = useDocument(params.id);
  const runOCR = useRunOCR();

  if (documentQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (documentQuery.isError || !documentQuery.data) {
    return (
      <AppShell>
        <ErrorState
          title="Documento não encontrado"
          description="Confirme o identificador do documento e a disponibilidade do backend."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Detalhe do documento"
          description="A partir desta tela já é possível acionar OCR real sobre o documento selecionado."
        />
        <DocumentDetail
          document={documentQuery.data}
          onRunOCR={async () => {
            try {
              await runOCR.mutateAsync(documentQuery.data!.id);
            } catch {
              toast.error("Não foi possível iniciar OCR para este documento.");
            }
          }}
        />
      </div>
    </AppShell>
  );
}
