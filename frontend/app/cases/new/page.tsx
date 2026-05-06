"use client";

import { AppShell } from "@/components/layout/app-shell";
import { CaseForm } from "@/components/cases/case-form";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";

export default function NewCasePage() {
  const { activeOrganizationId } = useActiveOrganization();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Novo processo"
          description="Criação de processo respeitando cliente, advogado, organização ativa e validações DRF."
        />
        {!activeOrganizationId ? (
          <EmptyState
            title="Selecione uma organização"
            description="Selecione uma organização antes de criar um processo."
          />
        ) : (
          <CaseForm />
        )}
      </div>
    </AppShell>
  );
}
