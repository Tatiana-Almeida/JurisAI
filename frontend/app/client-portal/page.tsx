"use client";

import { AppShell } from "@/components/layout/app-shell";
import { ClientPortalHome } from "@/components/client-portal/client-portal-home";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useClientPortalData } from "@/hooks/use-jurisai-queries";

export default function ClientPortalPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const clientPortalQuery = useClientPortalData();

  if (!activeOrganizationId) {
    return (
      <AppShell portalOnly>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar o portal do cliente deste tenant."
        />
      </AppShell>
    );
  }

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
            description="Confirme autenticacao, organizacao ativa e endpoints do client portal."
          />
        ) : null}
        {!clientPortalQuery.isLoading && !clientPortalQuery.isError ? (
          <ClientPortalHome
            cases={clientPortalQuery.data?.cases ?? []}
            documents={clientPortalQuery.data?.documents ?? []}
            messagesCount={clientPortalQuery.data?.messages.length ?? 0}
          />
        ) : null}
      </div>
    </AppShell>
  );
}
