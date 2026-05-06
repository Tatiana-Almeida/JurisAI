"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ClientForm } from "@/components/clients/client-form";
import { ClientsTable } from "@/components/clients/clients-table";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useClients } from "@/hooks/use-jurisai-queries";

export default function ClientsPage() {
  const clientsQuery = useClients();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Clientes"
          description="A UI usa o backend real de utilizadores por organização e filtra clientes por papel, sem inventar um endpoint próprio."
        />
        <ClientForm />
        {clientsQuery.isLoading ? <LoadingSkeleton /> : null}
        {clientsQuery.isError ? (
          <ErrorState
            title="Não foi possível listar clientes"
            description="Confirme autenticação e disponibilidade de `/api/v1/users/`."
          />
        ) : null}
        {clientsQuery.data ? <ClientsTable clients={clientsQuery.data} /> : null}
      </div>
    </AppShell>
  );
}
