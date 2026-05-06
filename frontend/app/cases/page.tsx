"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { CasesTable } from "@/components/cases/cases-table";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useCases } from "@/hooks/use-jurisai-queries";

export default function CasesPage() {
  const casesQuery = useCases();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Processos"
          description="Gestão multi-tenant de processos jurídicos ligada ao endpoint real `/api/v1/cases/`."
          actions={
            <Button asChild>
              <Link href="/cases/new">Novo processo</Link>
            </Button>
          }
        />
        {casesQuery.isLoading ? <LoadingSkeleton /> : null}
        {casesQuery.isError ? (
          <ErrorState
            title="Não foi possível listar processos"
            description="Confirme autenticação, organização ativa e disponibilidade do backend."
          />
        ) : null}
        {casesQuery.data ? <CasesTable cases={casesQuery.data} /> : null}
      </div>
    </AppShell>
  );
}
