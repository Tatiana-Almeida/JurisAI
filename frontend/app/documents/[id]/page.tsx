"use client";

import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { AppShell } from "@/components/layout/app-shell";
import { DocumentDetail } from "@/components/documents/document-detail";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useDocument } from "@/hooks/use-documents";
import { useRunAdvancedOCR, useRunOCR } from "@/hooks/use-ocr";
import { getDRFErrorMessage } from "@/lib/errors/drf";

export default function DocumentDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const { activeOrganizationId } = useActiveOrganization();
  const documentQuery = useDocument(params.id);
  const runOCR = useRunOCR();
  const runAdvancedOCR = useRunAdvancedOCR();

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organização"
          description="Selecione uma organização para visualizar este documento."
        />
      </AppShell>
    );
  }

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
        <ModuleErrorState
          moduleName="documento"
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
          isRunningOCR={runOCR.isPending}
          isRunningAdvancedOCR={runAdvancedOCR.isPending}
          onRunOCR={async () => {
            try {
              await runOCR.mutateAsync(documentQuery.data!.id);
              router.push("/ocr");
            } catch (error) {
              toast.error("Não foi possível iniciar OCR para este documento.", {
                description: getDRFErrorMessage(error),
              });
            }
          }}
          onRunAdvancedOCR={async () => {
            try {
              await runAdvancedOCR.mutateAsync(documentQuery.data!.id);
              router.push("/ocr");
            } catch (error) {
              toast.error("Não foi possível iniciar OCR avançado para este documento.", {
                description: getDRFErrorMessage(error),
              });
            }
          }}
        />
      </div>
    </AppShell>
  );
}
