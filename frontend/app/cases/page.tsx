"use client";

import Link from "next/link";
import { useState } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { CasesTable } from "@/components/cases/cases-table";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useCases } from "@/hooks/use-cases";

export default function CasesPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<string>("all");
  const casesQuery = useCases({
    search: search || undefined,
    status: status === "all" ? undefined : status,
  });

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Processos"
          description="Gestao multi-tenant de processos juridicos ligada ao endpoint real `/api/v1/cases/` com filtros simples de busca e estado."
          actions={
            <Button asChild>
              <Link href="/cases/new">Novo processo</Link>
            </Button>
          }
        />
        {!activeOrganizationId ? (
          <EmptyState
            title="Selecione uma organizacao"
            description="Selecione uma organizacao para visualizar os processos deste tenant."
          />
        ) : (
          <>
            <div className="grid gap-3 md:grid-cols-[1fr_220px]">
              <Input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Buscar por titulo ou descricao"
              />
              <Select value={status} onValueChange={setStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="Filtrar por estado" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os estados</SelectItem>
                  <SelectItem value="open">open</SelectItem>
                  <SelectItem value="in_progress">in_progress</SelectItem>
                  <SelectItem value="closed">closed</SelectItem>
                  <SelectItem value="on_hold">on_hold</SelectItem>
                </SelectContent>
              </Select>
            </div>
            {casesQuery.isLoading ? <LoadingSkeleton /> : null}
            {casesQuery.isError ? (
              <ModuleErrorState
                moduleName="processos"
                description="Confirme autenticacao, organizacao ativa e disponibilidade do backend."
              />
            ) : null}
            {casesQuery.data ? <CasesTable cases={casesQuery.data} /> : null}
          </>
        )}
      </div>
    </AppShell>
  );
}
