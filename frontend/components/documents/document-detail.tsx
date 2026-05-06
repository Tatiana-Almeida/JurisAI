import Link from "next/link";
import type { Document } from "@/types/documents";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { DocumentTypeBadge } from "@/components/documents/document-type-badge";

type DocumentDetailProps = {
  document: Document;
  onRunOCR?: () => void;
};

export function DocumentDetail({ document, onRunOCR }: DocumentDetailProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="flex flex-row items-start justify-between gap-4">
        <div>
          <CardTitle>Documento {document.id.slice(0, 8)}</CardTitle>
          <p className="mt-2 text-sm text-muted-foreground">
            Caso: {document.law_case_id ?? "sem vínculo"} · Versão: {document.version ?? 1}
          </p>
        </div>
        <DocumentTypeBadge type={document.type} />
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="rounded-2xl border border-border/60 p-4 text-sm text-muted-foreground">
          {document.content?.trim() || "Conteúdo ainda vazio ou dependente de OCR."}
        </div>
        <div className="flex flex-wrap gap-3">
          <Button type="button" onClick={onRunOCR}>
            Executar OCR
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
