"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { mapDRFErrorsToForm } from "@/lib/errors/drf";
import { ragSettingsSchema } from "@/lib/validation/knowledge-base";
import { useUpdateRAGSettings } from "@/hooks/use-knowledge-base";
import type { RAGSettings } from "@/types/knowledge-base";
import type { z } from "zod";

type RAGSettingsPanelProps = {
  settings?: RAGSettings;
};

type RAGSettingsFormValues = z.infer<typeof ragSettingsSchema>;

export function RAGSettingsPanel({ settings }: RAGSettingsPanelProps) {
  const updateSettings = useUpdateRAGSettings();
  const form = useForm<RAGSettingsFormValues>({
    resolver: zodResolver(ragSettingsSchema),
    defaultValues: {
      retrieval_mode: settings?.retrieval_mode ?? "hybrid",
      external_embeddings_enabled: settings?.external_embeddings_enabled ?? false,
      embedding_provider: settings?.embedding_provider ?? "local",
      embedding_model: settings?.embedding_model ?? "local-hash-v1",
      require_human_review_for_ai_answers:
        settings?.require_human_review_for_ai_answers ?? true,
      allow_document_content_to_external_provider:
        settings?.allow_document_content_to_external_provider ?? false,
      max_sources_per_answer: settings?.max_sources_per_answer ?? 5,
      min_confidence_threshold: settings?.min_confidence_threshold ?? "0.30",
    },
  });

  useEffect(() => {
    form.reset({
      retrieval_mode: settings?.retrieval_mode ?? "hybrid",
      external_embeddings_enabled: settings?.external_embeddings_enabled ?? false,
      embedding_provider: settings?.embedding_provider ?? "local",
      embedding_model: settings?.embedding_model ?? "local-hash-v1",
      require_human_review_for_ai_answers:
        settings?.require_human_review_for_ai_answers ?? true,
      allow_document_content_to_external_provider:
        settings?.allow_document_content_to_external_provider ?? false,
      max_sources_per_answer: settings?.max_sources_per_answer ?? 5,
      min_confidence_threshold: settings?.min_confidence_threshold ?? "0.30",
    });
  }, [form, settings]);

  const usesLocalHash =
    !form.watch("embedding_provider") || form.watch("embedding_provider") === "local";

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="space-y-3">
        <CardTitle>RAG settings</CardTitle>
        {usesLocalHash ? (
          <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-sm text-amber-900 dark:text-amber-200">
            local-hash-v1 valida o pipeline de retrieval sem enviar dados para fora, mas nao e embedding semantico avancado.
          </div>
        ) : null}
      </CardHeader>
      <CardContent>
        <form
          className="grid gap-4"
          onSubmit={form.handleSubmit(async (values) => {
            form.clearErrors();
            try {
              await updateSettings.mutateAsync(values);
            } catch (error) {
              mapDRFErrorsToForm(error, form.setError);
            }
          })}
        >
          <div className="grid gap-4 md:grid-cols-2">
            <label className="space-y-2 text-sm">
              <span className="font-medium">Retrieval mode</span>
              <Input {...form.register("retrieval_mode")} />
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Embedding provider</span>
              <Input {...form.register("embedding_provider")} />
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Embedding model</span>
              <Input {...form.register("embedding_model")} />
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Max sources per answer</span>
              <Input type="number" {...form.register("max_sources_per_answer", { valueAsNumber: true })} />
            </label>
            <label className="space-y-2 text-sm md:col-span-2">
              <span className="font-medium">Min confidence threshold</span>
              <Input {...form.register("min_confidence_threshold")} />
            </label>
          </div>

          <div className="grid gap-3 rounded-2xl border border-border/60 p-4 text-sm">
            {[
              ["external_embeddings_enabled", "Permitir embeddings externos"],
              [
                "allow_document_content_to_external_provider",
                "Permitir envio de conteudo para provider externo",
              ],
              [
                "require_human_review_for_ai_answers",
                "Exigir revisao humana para respostas de IA",
              ],
            ].map(([fieldName, label]) => (
              <label key={fieldName} className="flex items-center gap-3">
                <input
                  type="checkbox"
                  className="size-4 rounded border-border"
                  checked={Boolean(form.watch(fieldName as keyof RAGSettingsFormValues))}
                  onChange={(event) =>
                    form.setValue(
                      fieldName as keyof RAGSettingsFormValues,
                      event.target.checked as never,
                      { shouldDirty: true },
                    )
                  }
                />
                <span>{label}</span>
              </label>
            ))}
          </div>

          {form.formState.errors.root ? (
            <p className="text-sm text-destructive">{form.formState.errors.root.message}</p>
          ) : null}

          <div className="flex justify-end">
            <Button type="submit" disabled={updateSettings.isPending}>
              {updateSettings.isPending ? "A guardar..." : "Guardar configuracoes"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
