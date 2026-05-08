"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useKnowledgeBaseSearch } from "@/hooks/use-knowledge-base";
import { mapDRFErrorsToForm } from "@/lib/errors/drf";
import { knowledgeBaseSearchSchema } from "@/lib/validation/knowledge-base";
import type { z } from "zod";

type KBSearchProps = {
  knowledgeBaseId?: string;
};

type SearchFormValues = z.infer<typeof knowledgeBaseSearchSchema>;

export function KBSearch({ knowledgeBaseId }: KBSearchProps) {
  const searchMutation = useKnowledgeBaseSearch(knowledgeBaseId);
  const form = useForm<SearchFormValues>({
    resolver: zodResolver(knowledgeBaseSearchSchema),
    defaultValues: {
      query: "",
    },
  });

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Search</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <form
          className="flex flex-col gap-3 lg:flex-row"
          onSubmit={form.handleSubmit(async (values) => {
            form.clearErrors();
            try {
              await searchMutation.mutateAsync({ ...values, limit: 5 });
            } catch (error) {
              mapDRFErrorsToForm(error, form.setError);
            }
          })}
        >
          <div className="flex-1 space-y-2">
            <Input {...form.register("query")} placeholder="Pesquisar documentos e trechos relevantes" />
            <p className="text-xs text-destructive">{form.formState.errors.query?.message}</p>
          </div>
          <Button type="submit" disabled={!knowledgeBaseId || searchMutation.isPending}>
            {searchMutation.isPending ? "A pesquisar..." : "Pesquisar"}
          </Button>
        </form>
        {form.formState.errors.root ? (
          <p className="text-sm text-destructive">{form.formState.errors.root.message}</p>
        ) : null}
        {searchMutation.data?.sources?.length ? (
          <div className="space-y-3">
            {searchMutation.data.sources.map((source, index) => (
              <div key={`${source.document_id ?? "doc"}-${index}`} className="rounded-2xl border border-border/60 p-4 text-sm">
                <div className="font-medium">{source.title ?? `Resultado ${index + 1}`}</div>
                <div className="mt-1 text-muted-foreground">{source.excerpt ?? "Sem trecho."}</div>
                <div className="mt-2 text-xs text-muted-foreground">
                  documento={source.document_id ?? "n/d"} · score={String(source.final_score ?? "n/d")}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            Os resultados de pesquisa aparecerao aqui com score, documento e trecho associado.
          </p>
        )}
      </CardContent>
    </Card>
  );
}
