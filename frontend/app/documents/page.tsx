"use client";

import { useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";
import { AppShell } from "@/components/layout/app-shell";
import { DocumentUploadDropzone } from "@/components/documents/document-upload-dropzone";
import { DocumentsTable } from "@/components/documents/documents-table";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
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
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useCases } from "@/hooks/use-cases";
import { useDocuments, useUploadDocument } from "@/hooks/use-documents";
import { getDRFErrorMessage, mapDRFErrorsToForm } from "@/lib/errors/drf";
import { documentSchema } from "@/lib/validation/documents";

type DocumentFormValues = z.infer<typeof documentSchema>;

export default function DocumentsPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadProgress, setUploadProgress] = useState<number | null>(null);
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

  const selectedCaseId = useWatch({ control: form.control, name: "law_case_id" });
  const selectedType = useWatch({ control: form.control, name: "type" });
  const effectiveProgress = useMemo(
    () => (uploadDocument.isPending ? uploadProgress ?? 0 : uploadProgress),
    [uploadDocument.isPending, uploadProgress],
  );

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Documentos"
          description="Upload juridico com validacao alinhada ao serializer real de documentos e gatilhos reais para OCR."
        />
        {!activeOrganizationId ? (
          <EmptyState
            title="Selecione uma organizacao"
            description="Selecione uma organizacao para listar e enviar documentos deste tenant."
          />
        ) : (
          <>
            <Card className="jurisai-panel rounded-3xl">
              <CardHeader>
                <CardTitle>Novo upload</CardTitle>
              </CardHeader>
              <CardContent className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
                <DocumentUploadDropzone
                  onFilesAccepted={(files) => setSelectedFiles(files)}
                  uploadProgress={effectiveProgress}
                  helperText="O serializer aceita PDF, DOCX, TXT, PNG, JPG e JPEG, com validacao binaria e limite de 10 MB."
                />
                <form
                  className="space-y-4"
                  onSubmit={form.handleSubmit(async (values) => {
                    if (!selectedFiles[0]) {
                      toast.error("Selecione um ficheiro antes de enviar.");
                      return;
                    }

                    const formData = new FormData();
                    formData.append("law_case_id", values.law_case_id);
                    formData.append("type", values.type);
                    formData.append("content", values.content ?? "");
                    formData.append("file", selectedFiles[0]);

                    try {
                      setUploadProgress(0);
                      await uploadDocument.mutateAsync({
                        formData,
                        onUploadProgress: (event) => {
                          if (!event.total) {
                            return;
                          }
                          setUploadProgress(Math.round((event.loaded / event.total) * 100));
                        },
                      });
                      setSelectedFiles([]);
                      setUploadProgress(null);
                      form.reset({
                        law_case_id: "",
                        type: "petition",
                        content: "",
                      });
                    } catch (error) {
                      mapDRFErrorsToForm(error, form.setError);
                      const status = (error as { status?: number })?.status;
                      const description =
                        status === 413
                          ? "O ficheiro excede o limite de tamanho aceite pelo backend."
                          : status === 415
                            ? "O backend rejeitou o formato do ficheiro enviado."
                            : getDRFErrorMessage(error);
                      toast.error("Upload falhou.", {
                        description,
                      });
                    } finally {
                      setUploadProgress(null);
                    }
                  })}
                >
                  <div className="space-y-2">
                    <Label>Processo</Label>
                    <Select
                      value={selectedCaseId}
                      onValueChange={(value) => form.setValue("law_case_id", value)}
                    >
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
                    {form.formState.errors.law_case_id ? (
                      <p className="text-sm text-destructive">
                        {form.formState.errors.law_case_id.message}
                      </p>
                    ) : null}
                  </div>
                  <div className="space-y-2">
                    <Label>Tipo</Label>
                    <Select
                      value={selectedType}
                      onValueChange={(value) =>
                        form.setValue("type", value as DocumentFormValues["type"])
                      }
                    >
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
                    <Label htmlFor="document-content">Conteudo inicial</Label>
                    <Input id="document-content" {...form.register("content")} />
                  </div>
                  {form.formState.errors.root?.message ? (
                    <p className="rounded-2xl bg-destructive/10 px-4 py-3 text-sm text-destructive">
                      {form.formState.errors.root.message}
                    </p>
                  ) : null}
                  <Button
                    type="submit"
                    disabled={uploadDocument.isPending || !activeOrganizationId}
                  >
                    {uploadDocument.isPending ? "A enviar..." : "Enviar documento"}
                  </Button>
                </form>
              </CardContent>
            </Card>
            {documentsQuery.isLoading ? <LoadingSkeleton /> : null}
            {documentsQuery.isError ? (
              <ModuleErrorState
                moduleName="documentos"
                description="Confirme autenticacao, organizacao ativa e disponibilidade do endpoint de documentos."
              />
            ) : null}
            {documentsQuery.data ? <DocumentsTable documents={documentsQuery.data} /> : null}
          </>
        )}
      </div>
    </AppShell>
  );
}
