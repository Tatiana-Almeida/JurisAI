"use client";

import { useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { endpoints } from "@/lib/api/endpoints";
import { apiClient } from "@/lib/api/client";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { loginSchema, type LoginInput } from "@/lib/validation/auth";
import { useAuthStore } from "@/stores/auth-store";

export function LoginForm() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated);

  const form = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  async function onSubmit(values: LoginInput) {
    setIsSubmitting(true);
    form.clearErrors();

    try {
      const response = await apiClient.post(endpoints.auth.login, values);
      const tokens = {
        access: response.data.access,
        refresh: response.data.refresh,
      };

      setAuthenticated({
        user: {
          email: values.email,
          name: values.email,
        },
        tokens,
      });

      toast.success("Sessão iniciada.", {
        description:
          "A autenticação usa localStorage nesta fase. Migrar para cookies httpOnly fica como hardening futuro.",
      });

      router.push("/dashboard");
    } catch (error) {
      mapDRFErrorsToForm(error, form.setError);
      toast.error("Não foi possível entrar.", {
        description: getDRFErrorMessage(error),
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Card className="jurisai-panel w-full max-w-lg rounded-[2rem]">
      <CardHeader className="space-y-4">
        <Image
          src="/brand/jurisai-logo.png"
          alt="JurisAI"
          width={160}
          height={48}
          className="h-12 w-auto"
        />
        <div className="space-y-1">
          <CardTitle className="text-2xl">Entrar no JurisAI</CardTitle>
          <p className="text-sm leading-6 text-muted-foreground">
            Foundation de autenticação com JWT, React Hook Form e mapeamento de erros DRF.
          </p>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" {...form.register("email")} />
            {form.formState.errors.email ? (
              <p className="text-sm text-destructive">
                {form.formState.errors.email.message}
              </p>
            ) : null}
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" {...form.register("password")} />
            {form.formState.errors.password ? (
              <p className="text-sm text-destructive">
                {form.formState.errors.password.message}
              </p>
            ) : null}
          </div>

          {form.formState.errors.root?.message ? (
            <p className="rounded-2xl bg-destructive/10 px-4 py-3 text-sm text-destructive">
              {form.formState.errors.root.message}
            </p>
          ) : null}

          <Button className="w-full rounded-full" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "A entrar..." : "Entrar"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
