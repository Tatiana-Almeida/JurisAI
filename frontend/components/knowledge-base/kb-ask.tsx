"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { SourcesList } from "@/components/knowledge-base/sources-list";
import { knowledgeBaseSearchSchema } from "@/lib/validation/knowledge-base";
import { mapDRFErrorsToForm } from "@/lib/errors/drf";
import { useAskKnowledgeBase } from "@/hooks/use-knowledge-base";
import type { z } from "zod";

type KBAskProps = {
  knowledgeBaseId?: string;
};

type AskFormValues = z.infer<typeof knowledgeBaseSearchSchema>;

export function KBAsk({ knowledgeBaseId }: KBAskProps) {
  const askMutation = useAskKnowledgeBase(knowledgeBaseId);
  const form = useForm<AskFormValues>({
    resolver: zodResolver(knowledgeBaseSearchSchema),
    defaultValues: {
      query: "",
    },
  });

  const usesLocalHash =
    !askMutation.data?.retrieval_method ||
    askMutation.data.retrieval_method.includes("local") ||
    askMutation.data.effective_retrieval_mode?.includes("local");

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Perguntar a base</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <form
          className="flex flex-col gap-3 lg:flex-row"
          onSubmit={form.handleSubmit(async (values) => {
            form.clearErrors();
            try {
              await askMutation.mutateAsync({ ...values, limit: 5 });
            } catch (error) {
              mapDRFErrorsToForm(error, form.setError);
            }
          })}
        >
          <div className="flex-1 space-y-2">
            <Input
              {...form.register("query")}
              placeholder="Pergunta juridica com contexto multi-tenant"
            />
            <p className="text-xs text-destructive">{form.formState.errors.query?.message}</p>
          </div>
          <Button type="submit" disabled={!knowledgeBaseId || askMutation.isPending}>
            {askMutation.isPending ? "A consultar..." : "Perguntar"}
          </Button>
        </form>

        {form.formState.errors.root ? (
          <p className="text-sm text-destructive">{form.formState.errors.root.message}</p>
        ) : null}

        {askMutation.data ? (
          <div className="space-y-4 rounded-2xl border border-border/60 p-4 text-sm">
            <div className="flex flex-wrap items-center gap-3">
              <div className="font-medium">Resposta</div>
              <div className="rounded-full bg-primary/10 px-3 py-1 text-xs text-primary">
                confidence={String(askMutation.data.confidence ?? "n/d")}
              </div>
              <div className="rounded-full bg-muted px-3 py-1 text-xs text-muted-foreground">
                retrieval_method={askMutation.data.retrieval_method ?? "n/d"}
              </div>
            </div>
            <div className="whitespace-pre-wrap text-muted-foreground">
              {askMutation.data.answer ?? "Sem resposta."}
            </div>
            {Number(askMutation.data.confidence ?? 0) < 0.4 ? (
              <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-amber-900 dark:text-amber-200">
                Confianca baixa. Recomenda-se validacao humana antes de reutilizar a resposta.
              </div>
            ) : null}
            {usesLocalHash ? (
              <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-amber-900 dark:text-amber-200">
                local-hash-v1 valida o pipeline local sem enviar dados para fora, mas nao equivale a embeddings semanticos avancados.
              </div>
            ) : null}
            <SourcesList
              sources={askMutation.data.sources ?? []}
              confidence={askMutation.data.confidence}
              retrievalMethod={askMutation.data.retrieval_method}
              fallbackUsed={askMutation.data.fallback_used}
              fallbackReason={askMutation.data.fallback_reason}
            />
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            A resposta aparecera com fontes, confianca e fallback explicito quando o endpoint devolver dados.
          </p>
        )}
      </CardContent>
    </Card>
  );
}
