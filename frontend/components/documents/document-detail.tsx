import Link from "next/link";
import type { Document } from "@/types/documents";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DocumentTypeBadge } from "@/components/documents/document-type-badge";

type DocumentDetailProps = {
  document: Document;
  isRunningOCR?: boolean;
  isRunningAdvancedOCR?: boolean;
  onRunOCR?: () => void;
  onRunAdvancedOCR?: () => void;
};

export function DocumentDetail({
  document,
  isRunningOCR = false,
  isRunningAdvancedOCR = false,
  onRunOCR,
  onRunAdvancedOCR,
}: DocumentDetailProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="flex flex-row items-start justify-between gap-4">
        <div>
          <CardTitle>Documento {document.id.slice(0, 8)}</CardTitle>
          <p className="mt-2 text-sm text-muted-foreground">
            Processo: {document.law_case_id ?? document.law_case ?? "sem vínculo"} · Versão:{" "}
            {document.version ?? 1}
          </p>
        </div>
        <DocumentTypeBadge type={document.type} />
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="rounded-2xl border border-border/60 p-4 text-sm text-muted-foreground">
          {document.content?.trim() || "Conteúdo ainda vazio ou dependente de OCR."}
        </div>
        <div className="rounded-2xl border border-primary/20 bg-primary/5 p-4 text-sm text-muted-foreground">
          OCR textual usa o fluxo local/base. O modo avançado respeita as definições do tenant,
          mas OCR externo continua desativado por padrão.
        </div>
        <div className="flex flex-wrap gap-3">
          <Button type="button" onClick={onRunOCR} disabled={isRunningOCR || isRunningAdvancedOCR}>
            {isRunningOCR ? "A iniciar OCR..." : "Executar OCR"}
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={onRunAdvancedOCR}
            disabled={isRunningOCR || isRunningAdvancedOCR}
          >
            {isRunningAdvancedOCR ? "A iniciar OCR avançado..." : "Executar OCR avançado"}
          </Button>
          <Button asChild variant="outline">
            <Link href="/ocr">Ver jobs OCR</Link>
          </Button>
          {document.file ? (
            <Button asChild variant="outline">
              <Link href={document.file} target="_blank">
                Abrir ficheiro
              </Link>
            </Button>
          ) : null}
        </div>
      </CardContent>
    </Card>
  );
}
