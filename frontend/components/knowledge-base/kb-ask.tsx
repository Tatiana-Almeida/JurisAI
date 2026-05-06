"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAskKnowledgeBase } from "@/hooks/use-jurisai-queries";

type KBAskProps = {
  knowledgeBaseId?: string;
};

export function KBAsk({ knowledgeBaseId }: KBAskProps) {
  const [query, setQuery] = useState("");
  const askMutation = useAskKnowledgeBase(knowledgeBaseId);

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Perguntar à base</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-3">
          <Input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Pergunta jurídica com contexto multi-tenant"
          />
          <Button
            type="button"
            disabled={!knowledgeBaseId || askMutation.isPending || !query.trim()}
            onClick={() => askMutation.mutate({ query, limit: 5 })}
          >
            {askMutation.isPending ? "A consultar..." : "Perguntar"}
          </Button>
        </div>
        {askMutation.data ? (
          <div className="space-y-3 rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">Resposta</div>
            <div className="text-muted-foreground">{askMutation.data.answer ?? "Sem resposta."}</div>
            <div className="text-muted-foreground">
              confidence={askMutation.data.confidence ?? "n/a"} · retrieval_method={askMutation.data.retrieval_method ?? "n/a"}
            </div>
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            A resposta aparecerá com fontes, confiança e fallback explícito quando o endpoint devolver dados.
          </p>
        )}
      </CardContent>
    </Card>
  );
}
