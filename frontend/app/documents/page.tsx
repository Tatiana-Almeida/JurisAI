"use client";

import { useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { DocumentsTable } from "@/components/documents/documents-table";
import { DocumentUploadDropzone } from "@/components/documents/document-upload-dropzone";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useCases, useDocuments, useUploadDocument } from "@/hooks/use-jurisai-queries";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { documentSchema } from "@/lib/validation/documents";
import type { z } from "zod";

type DocumentFormValues = z.infer<typeof documentSchema>;

export default function DocumentsPage() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const casesQuery = useCases();
  const documentsQuery = useDocuments();
  const uploadDocument = useUploadDocument();

  const form = useForm<DocumentFormValues>({
    resolver: zodResolver(documentSchema),
    defaultValues: {
      law_case_id: "",
      type: "petition",
      content: "",
    },
  });

  const uploadProgress = useMemo(() => (uploadDocument.isPending ? 70 : selectedFiles.length ? 100 : null), [selectedFiles.length, uploadDocument.isPending]);

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Documentos"
          description="Upload jurídico com validação alinhada ao serializer de documentos e gatilhos reais para OCR."
        />
        <Card className="jurisai-panel rounded-3xl">
          <CardHeader>
            <CardTitle>Novo upload</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
            <DocumentUploadDropzone
              onFilesAccepted={(files) => setSelectedFiles(files)}
              uploadProgress={uploadProgress}
              helperText="O serializer aceita PDF, DOCX, TXT, PNG, JPG e JPEG, com validação binária e limite de 10 MB."
            />
            <form
              className="space-y-4"
              onSubmit={form.handleSubmit(async (values) => {
                if (!selectedFiles[0]) {
                  toast.error("Selecione um ficheiro antes de enviar.");
                  return;
                }

                const payload = new FormData();
                payload.append("law_case_id", values.law_case_id);
                payload.append("type", values.type);
                payload.append("content", values.content ?? "");
                payload.append("file", selectedFiles[0]);

                try {
                  await uploadDocument.mutateAsync(payload);
                  setSelectedFiles([]);
                  form.reset({
                    law_case_id: "",
                    type: "petition",
                    content: "",
                  });
                } catch (error) {
                  mapDRFErrorsToForm(error, form.setError);
                  toast.error("Upload falhou.", {
                    description: getDRFErrorMessage(error),
                  });
                }
              })}
            >
              <div className="space-y-2">
                <Label>Processo</Label>
                <Select value={form.watch("law_case_id")} onValueChange={(value) => form.setValue("law_case_id", value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecionar processo" />
                  </SelectTrigger>
                  <SelectContent>
                    {(casesQuery.data ?? []).map((lawCase) => (
                      <SelectItem key={lawCase.id} value={lawCase.id}>
                        {lawCase.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Tipo</Label>
                <Select value={form.watch("type")} onValueChange={(value) => form.setValue("type", value as DocumentFormValues["type"])}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="petition">petition</SelectItem>
                    <SelectItem value="contract">contract</SelectItem>
                    <SelectItem value="evidence">evidence</SelectItem>
                    <SelectItem value="internal">internal</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="document-content">Conteúdo inicial</Label>
                <Input id="document-content" {...form.register("content")} />
              </div>
              <Button type="submit" disabled={uploadDocument.isPending}>
                {uploadDocument.isPending ? "A enviar..." : "Enviar documento"}
              </Button>
            </form>
          </CardContent>
        </Card>
        {documentsQuery.isLoading ? <LoadingSkeleton /> : null}
        {documentsQuery.isError ? (
          <ErrorState
            title="Não foi possível listar documentos"
            description="Confirme autenticação, organização ativa e disponibilidade do endpoint de documentos."
          />
        ) : null}
        {documentsQuery.data ? <DocumentsTable documents={documentsQuery.data} /> : null}
      </div>
    </AppShell>
  );
}
