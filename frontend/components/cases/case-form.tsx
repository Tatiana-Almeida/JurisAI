"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useClients, useCreateCase, useLawyers } from "@/hooks/use-jurisai-queries";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { caseSchema } from "@/lib/validation/cases";
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

type CaseFormValues = z.infer<typeof caseSchema>;

export function CaseForm() {
  const { activeOrganizationId } = useActiveOrganization();
  const createCase = useCreateCase();
  const clientsQuery = useClients();
  const lawyersQuery = useLawyers();
  const form = useForm<CaseFormValues>({
    resolver: zodResolver(caseSchema),
    defaultValues: {
      title: "",
      description: "",
      status: "open",
      client_id: "",
      lawyer_id: "",
    },
  });
  const clientId = useWatch({ control: form.control, name: "client_id" });
  const lawyerId = useWatch({ control: form.control, name: "lawyer_id" });
  const status = useWatch({ control: form.control, name: "status" });

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Novo processo</CardTitle>
      </CardHeader>
      <CardContent>
        <form
          className="grid gap-4 md:grid-cols-2"
          onSubmit={form.handleSubmit(async (values) => {
            try {
              await createCase.mutateAsync(values);
              form.reset({
                title: "",
                description: "",
                status: "open",
                client_id: "",
                lawyer_id: "",
              });
            } catch (error) {
              mapDRFErrorsToForm(error, form.setError);
              toast.error("Não foi possível criar o processo.", {
                description: getDRFErrorMessage(error),
              });
            }
          })}
        >
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="case-title">Título</Label>
            <Input id="case-title" {...form.register("title")} />
            {form.formState.errors.title ? (
              <p className="text-sm text-destructive">{form.formState.errors.title.message}</p>
            ) : null}
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="case-description">Descrição</Label>
            <Textarea id="case-description" rows={4} {...form.register("description")} />
            {form.formState.errors.description ? (
              <p className="text-sm text-destructive">
                {form.formState.errors.description.message}
              </p>
            ) : null}
          </div>
          <div className="space-y-2">
            <Label>Cliente</Label>
            <Select value={clientId} onValueChange={(value) => form.setValue("client_id", value)}>
              <SelectTrigger>
                <SelectValue placeholder="Selecionar cliente" />
              </SelectTrigger>
              <SelectContent>
                {(clientsQuery.data ?? []).map((client) => (
                  <SelectItem key={client.id} value={client.id}>
                    {client.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {form.formState.errors.client_id ? (
              <p className="text-sm text-destructive">
                {form.formState.errors.client_id.message}
              </p>
            ) : null}
          </div>
          <div className="space-y-2">
            <Label>Advogado</Label>
            <Select value={lawyerId} onValueChange={(value) => form.setValue("lawyer_id", value)}>
              <SelectTrigger>
                <SelectValue placeholder="Selecionar advogado" />
              </SelectTrigger>
              <SelectContent>
                {(lawyersQuery.data ?? []).map((lawyer) => (
                  <SelectItem key={lawyer.id!} value={lawyer.id!}>
                    {lawyer.name ?? lawyer.email}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {form.formState.errors.lawyer_id ? (
              <p className="text-sm text-destructive">
                {form.formState.errors.lawyer_id.message}
              </p>
            ) : null}
          </div>
          <div className="space-y-2">
            <Label>Estado</Label>
            <Select
              value={status}
              onValueChange={(value) => form.setValue("status", value as CaseFormValues["status"])}
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
            <Button
              type="submit"
              disabled={
                createCase.isPending ||
                !activeOrganizationId ||
                clientsQuery.isLoading ||
                lawyersQuery.isLoading
              }
            >
              {createCase.isPending ? "A criar..." : "Criar processo"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
