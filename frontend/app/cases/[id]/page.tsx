"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useParams } from "next/navigation";
import { useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";
import { AppShell } from "@/components/layout/app-shell";
import { CaseStatusBadge } from "@/components/cases/case-status-badge";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useCase, useUpdateCase } from "@/hooks/use-cases";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { caseUpdateSchema } from "@/lib/validation/cases";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

type CaseUpdateValues = z.infer<typeof caseUpdateSchema>;

export default function CaseDetailPage() {
  const params = useParams<{ id: string }>();
  const { activeOrganizationId } = useActiveOrganization();
  const caseQuery = useCase(params.id);
  const updateCase = useUpdateCase(params.id);
  const form = useForm<CaseUpdateValues>({
    resolver: zodResolver(caseUpdateSchema),
    values: {
      title: caseQuery.data?.title ?? "",
      description: caseQuery.data?.description ?? "",
      status:
        (caseQuery.data?.status as CaseUpdateValues["status"] | undefined) ?? "open",
    },
  });
  const status = useWatch({ control: form.control, name: "status" });

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organização"
          description="Selecione uma organização para visualizar este processo."
        />
      </AppShell>
    );
  }

  if (caseQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (caseQuery.isError || !caseQuery.data) {
    return (
      <AppShell>
        <ModuleErrorState
          moduleName="processo"
          title="Processo não encontrado"
          description="Confirme o identificador do processo e a disponibilidade do backend."
        />
      </AppShell>
    );
  }

  const lawCase = caseQuery.data;

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title={lawCase.title}
          description={lawCase.description || "Sem descrição detalhada para este processo."}
          actions={<CaseStatusBadge status={lawCase.status} />}
        />
        <div className="jurisai-panel rounded-3xl p-6 text-sm text-muted-foreground">
          Cliente: {lawCase.client?.name ?? "N/D"} · Advogado: {lawCase.lawyer?.name ?? "N/D"} ·
          Organização: {lawCase.organization_id ?? "N/D"}
        </div>
        <Card className="jurisai-panel rounded-3xl">
          <CardHeader>
            <CardTitle>Editar metadados do processo</CardTitle>
          </CardHeader>
          <CardContent>
            <form
              className="grid gap-4 md:grid-cols-2"
              onSubmit={form.handleSubmit(async (values) => {
                try {
                  await updateCase.mutateAsync(values);
                  toast.success("Processo atualizado.");
                } catch (error) {
                  mapDRFErrorsToForm(error, form.setError);
                  toast.error("Não foi possível atualizar o processo.", {
                    description: getDRFErrorMessage(error),
                  });
                }
              })}
            >
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="case-title">Título</Label>
                <Input id="case-title" {...form.register("title")} />
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="case-description">Descrição</Label>
                <Textarea id="case-description" rows={4} {...form.register("description")} />
              </div>
              <div className="space-y-2">
                <Label>Estado</Label>
                <Select
                  value={status}
                  onValueChange={(value) =>
                    form.setValue("status", value as CaseUpdateValues["status"])
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="open">open</SelectItem>
                    <SelectItem value="in_progress">in_progress</SelectItem>
                    <SelectItem value="closed">closed</SelectItem>
                    <SelectItem value="on_hold">on_hold</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              {form.formState.errors.root?.message ? (
                <p className="md:col-span-2 rounded-2xl bg-destructive/10 px-4 py-3 text-sm text-destructive">
                  {form.formState.errors.root.message}
                </p>
              ) : null}
              <div className="md:col-span-2">
                <Button type="submit" disabled={updateCase.isPending}>
                  {updateCase.isPending ? "A guardar..." : "Guardar alterações"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </AppShell>
  );
}
