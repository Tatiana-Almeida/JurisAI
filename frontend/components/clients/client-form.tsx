"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateClient } from "@/hooks/use-jurisai-queries";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { clientSchema } from "@/lib/validation/clients";

type ClientFormValues = z.infer<typeof clientSchema>;

export function ClientForm() {
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
          </div>
          <div className="space-y-2">
            <Label htmlFor="client-email">Email</Label>
            <Input id="client-email" type="email" {...form.register("email")} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="client-password">Password inicial</Label>
            <Input id="client-password" type="password" {...form.register("password")} />
          </div>
          <div className="md:col-span-3">
            <Button type="submit" disabled={createClient.isPending}>
              {createClient.isPending ? "A criar..." : "Criar cliente"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
