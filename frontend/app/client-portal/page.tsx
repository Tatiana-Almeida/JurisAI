"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ClientPortalHome } from "@/components/client-portal/client-portal-home";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useClientPortalData } from "@/hooks/use-jurisai-queries";

export default function ClientPortalPage() {
  const clientPortalQuery = useClientPortalData();

  return (
    <AppShell portalOnly>
      <div className="space-y-8">
        <PageHeader
          title="Portal do Cliente"
          description="Foundation funcional baseada nos endpoints reais de casos, documentos e mensagens do client portal."
        />
        {clientPortalQuery.isLoading ? <LoadingSkeleton /> : null}
        {clientPortalQuery.isError ? (
          <ModuleErrorState
            moduleName="client-portal"
            description="Confirme autenticação, organização ativa e endpoints do client portal."
          />
        ) : null}
        {clientPortalQuery.data ? (
          <ClientPortalHome
            cases={clientPortalQuery.data.cases}
            documents={clientPortalQuery.data.documents}
          />
        ) : null}
      </div>
    </AppShell>
  );
}
