import Link from "next/link";
import type { Document } from "@/types/documents";
import type { OCRJob, OCRKnowledgeBasePipelineRun, OCRResult } from "@/types/ocr";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DocumentTypeBadge } from "@/components/documents/document-type-badge";
import { OCRStatusBadge } from "@/components/ocr/ocr-status-badge";

type DocumentDetailProps = {
  document: Document;
  latestJob?: OCRJob;
  latestResult?: OCRResult;
  latestPipeline?: OCRKnowledgeBasePipelineRun;
  isRunningOCR?: boolean;
  isRunningAdvancedOCR?: boolean;
  isApplyingOCR?: boolean;
  isRunningPipeline?: boolean;
  onRunOCR?: () => void;
  onRunAdvancedOCR?: () => void;
  onApplyOCRResult?: () => void;
  onRunPipeline?: () => void;
};

export function DocumentDetail({
  document,
  latestJob,
  latestResult,
  latestPipeline,
  isRunningOCR = false,
  isRunningAdvancedOCR = false,
  isApplyingOCR = false,
  isRunningPipeline = false,
  onRunOCR,
  onRunAdvancedOCR,
  onApplyOCRResult,
  onRunPipeline,
}: DocumentDetailProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="flex flex-row items-start justify-between gap-4">
        <div>
          <CardTitle>Documento {document.id.slice(0, 8)}</CardTitle>
          <p className="mt-2 text-sm text-muted-foreground">
            Processo: {document.law_case_id ?? document.law_case ?? "sem vinculo"} · Versao: {document.version ?? 1}
          </p>
        </div>
        <DocumentTypeBadge type={document.type} />
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="rounded-2xl border border-border/60 p-4 text-sm text-muted-foreground">
          {document.content?.trim() || "Conteudo ainda vazio ou dependente de OCR."}
        </div>
        <div className="rounded-2xl border border-primary/20 bg-primary/5 p-4 text-sm text-muted-foreground">
          OCR textual usa o fluxo local/base. O modo avancado respeita as definicoes do tenant,
          mas OCR externo continua desativado por padrao.
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">Ultimo job</div>
            {latestJob ? (
              <div className="mt-2 space-y-2 text-muted-foreground">
                <OCRStatusBadge status={latestJob.status} />
                <div>metodo: {latestJob.extraction_method ?? "local"}</div>
                <div>criado em: {latestJob.created_at ?? "n/d"}</div>
                {latestJob.error_message ? <div className="text-destructive">{latestJob.error_message}</div> : null}
              </div>
            ) : (
              <p className="mt-2 text-muted-foreground">Sem jobs associados ainda.</p>
            )}
          </div>
          <div className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">Ultimo resultado</div>
            {latestResult ? (
              <div className="mt-2 space-y-2 text-muted-foreground">
                <div>chars: {latestResult.char_count ?? 0}</div>
                <div>confidence: {String(latestResult.metadata?.confidence ?? "n/d")}</div>
                <div>resultado: {latestResult.id.slice(0, 8)}</div>
              </div>
            ) : (
              <p className="mt-2 text-muted-foreground">Sem resultado OCR ainda.</p>
            )}
          </div>
          <div className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">Ultimo pipeline KB</div>
            {latestPipeline ? (
              <div className="mt-2 space-y-2 text-muted-foreground">
                <OCRStatusBadge status={latestPipeline.status} />
                <div>advanced: {String(latestPipeline.used_advanced_ocr ?? false)}</div>
                <div>indexing_job: {latestPipeline.indexing_job ?? "n/d"}</div>
              </div>
            ) : (
              <p className="mt-2 text-muted-foreground">Sem pipeline para Knowledge Base ainda.</p>
            )}
          </div>
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
            {isRunningAdvancedOCR ? "A iniciar OCR avancado..." : "Executar OCR avancado"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={onApplyOCRResult}
            disabled={!latestResult || isApplyingOCR}
          >
            {isApplyingOCR ? "A aplicar..." : "Aplicar resultado ao documento"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={onRunPipeline}
            disabled={isRunningPipeline}
          >
            {isRunningPipeline ? "A iniciar pipeline..." : "OCR → Knowledge Base"}
          </Button>
          <Button asChild variant="outline">
            <Link href={`/ocr?document=${document.id}`}>Ver jobs OCR</Link>
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
