"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useCreateClient } from "@/hooks/use-clients";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { clientSchema } from "@/lib/validation/clients";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type ClientFormValues = z.infer<typeof clientSchema>;

export function ClientForm() {
  const { activeOrganizationId } = useActiveOrganization();
  const createClient = useCreateClient();
  const form = useForm<ClientFormValues>({
    resolver: zodResolver(clientSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
    },
  });

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Novo cliente</CardTitle>
      </CardHeader>
      <CardContent>
        <form
          className="grid gap-4 md:grid-cols-3"
          onSubmit={form.handleSubmit(async (values) => {
            try {
              await createClient.mutateAsync({
                ...values,
                role: "cliente",
              });
              form.reset({
                name: "",
                email: "",
                password: "",
              });
            } catch (error) {
              mapDRFErrorsToForm(error, form.setError);
              toast.error("Não foi possível criar o cliente.", {
                description: getDRFErrorMessage(error),
              });
            }
          })}
        >
          <div className="space-y-2">
            <Label htmlFor="client-name">Nome</Label>
            <Input id="client-name" {...form.register("name")} />
            {form.formState.errors.name ? (
              <p className="text-sm text-destructive">{form.formState.errors.name.message}</p>
            ) : null}
          </div>
          <div className="space-y-2">
            <Label htmlFor="client-email">Email</Label>
            <Input id="client-email" type="email" {...form.register("email")} />
            {form.formState.errors.email ? (
              <p className="text-sm text-destructive">{form.formState.errors.email.message}</p>
            ) : null}
          </div>
          <div className="space-y-2">
            <Label htmlFor="client-password">Password inicial</Label>
            <Input id="client-password" type="password" {...form.register("password")} />
            {form.formState.errors.password ? (
              <p className="text-sm text-destructive">
                {form.formState.errors.password.message}
              </p>
            ) : null}
          </div>
          {form.formState.errors.root?.message ? (
            <p className="md:col-span-3 rounded-2xl bg-destructive/10 px-4 py-3 text-sm text-destructive">
              {form.formState.errors.root.message}
            </p>
          ) : null}
          <div className="md:col-span-3">
            <Button
              type="submit"
              disabled={createClient.isPending || !activeOrganizationId}
            >
              {createClient.isPending ? "A criar..." : "Criar cliente"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
