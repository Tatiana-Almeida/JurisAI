"use client";

import { AppShell } from "@/components/layout/app-shell";
import { ClientForm } from "@/components/clients/client-form";
import { ClientsTable } from "@/components/clients/clients-table";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useClients } from "@/hooks/use-clients";

export default function ClientsPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const clientsQuery = useClients();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Clientes"
          description="A UI usa o endpoint real `/api/v1/users/` com filtro por papel cliente, sem inventar um endpoint separado."
        />
        {!activeOrganizationId ? (
          <EmptyState
            title="Selecione uma organização"
            description="Selecione uma organização para visualizar e criar clientes deste tenant."
          />
        ) : (
          <>
            <ClientForm />
            {clientsQuery.isLoading ? <LoadingSkeleton /> : null}
            {clientsQuery.isError ? (
              <ModuleErrorState
                moduleName="clientes"
                description="Confirme autenticação e disponibilidade de `/api/v1/users/`."
              />
            ) : null}
            {clientsQuery.data ? <ClientsTable clients={clientsQuery.data} /> : null}
          </>
        )}
      </div>
    </AppShell>
  );
}
