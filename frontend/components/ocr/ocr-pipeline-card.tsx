"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { mapDRFErrorsToForm } from "@/lib/errors/drf";
import { ocrKnowledgeBasePipelineSchema } from "@/lib/validation/ocr";
import { useRunOCRToKnowledgeBasePipeline } from "@/hooks/use-ocr";
import type { OCRKnowledgeBasePipelineRun } from "@/types/ocr";
import type { z } from "zod";

type OCRPipelineCardProps = {
  initialDocumentId?: string;
  initialKnowledgeBaseId?: string;
  latestRun?: OCRKnowledgeBasePipelineRun;
};

type OCRPipelineFormValues = z.infer<typeof ocrKnowledgeBasePipelineSchema>;

export function OCRPipelineCard({
  initialDocumentId,
  initialKnowledgeBaseId,
  latestRun,
}: OCRPipelineCardProps) {
  const runPipeline = useRunOCRToKnowledgeBasePipeline();
  const form = useForm<OCRPipelineFormValues>({
    resolver: zodResolver(ocrKnowledgeBasePipelineSchema),
    defaultValues: {
      document_id: initialDocumentId ?? "",
      knowledge_base_id: initialKnowledgeBaseId ?? "",
      update_document_content: true,
    },
  });

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="space-y-3">
        <CardTitle>OCR para Knowledge Base</CardTitle>
        <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-sm text-amber-900 dark:text-amber-200">
          Este fluxo so atualiza Document.content com confirmacao explicita.
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <form
          className="grid gap-4"
          onSubmit={form.handleSubmit(async (values) => {
            form.clearErrors();
            try {
              await runPipeline.mutateAsync(values);
            } catch (error) {
              mapDRFErrorsToForm(error, form.setError);
            }
          })}
        >
          <label className="space-y-2 text-sm">
            <span className="font-medium">Documento</span>
            <Input {...form.register("document_id")} placeholder="UUID do documento" />
            <p className="text-xs text-destructive">{form.formState.errors.document_id?.message}</p>
          </label>
          <label className="space-y-2 text-sm">
            <span className="font-medium">Knowledge Base</span>
            <Input {...form.register("knowledge_base_id")} placeholder="UUID da Knowledge Base" />
            <p className="text-xs text-destructive">
              {form.formState.errors.knowledge_base_id?.message}
            </p>
          </label>
          <label className="flex items-center gap-3 rounded-xl border border-border/60 p-3 text-sm">
            <input
              type="checkbox"
              checked={Boolean(form.watch("update_document_content"))}
              onChange={(event) =>
                form.setValue("update_document_content", event.target.checked, {
                  shouldDirty: true,
                })
              }
            />
            <span>Confirmo a atualizacao de Document.content neste pipeline.</span>
          </label>
          {form.formState.errors.root ? (
            <p className="text-sm text-destructive">{form.formState.errors.root.message}</p>
          ) : null}
          <div className="flex justify-end">
            <Button type="submit" disabled={runPipeline.isPending}>
              {runPipeline.isPending ? "A iniciar..." : "Executar pipeline"}
            </Button>
          </div>
        </form>

        {latestRun ? (
          <div className="rounded-2xl border border-border/60 p-4 text-sm text-muted-foreground">
            <div className="font-medium text-foreground">Ultimo retorno</div>
            <div className="mt-2 grid gap-2 md:grid-cols-2">
              <div>status: {latestRun.status}</div>
              <div>used_advanced_ocr: {String(latestRun.used_advanced_ocr ?? false)}</div>
              <div>advanced_ocr_reason: {latestRun.advanced_ocr_reason ?? "n/d"}</div>
              <div>ocr_audit_log: {latestRun.ocr_audit_log ?? "n/d"}</div>
              <div>ocr_result: {latestRun.ocr_result ?? "n/d"}</div>
              <div>indexing_job: {latestRun.indexing_job ?? "n/d"}</div>
            </div>
            {latestRun.error_message ? (
              <p className="mt-3 text-destructive">{latestRun.error_message}</p>
            ) : null}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
