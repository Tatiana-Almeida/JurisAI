"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ocrSettingsSchema } from "@/lib/validation/ocr";
import { mapDRFErrorsToForm } from "@/lib/errors/drf";
import { useUpdateOCRSettings } from "@/hooks/use-ocr";
import type { OCRSettings } from "@/types/ocr";
import type { z } from "zod";

type OCRSettingsPanelProps = {
  settings?: OCRSettings;
};

type OCRSettingsFormValues = z.infer<typeof ocrSettingsSchema>;

const PROVIDERS = ["local", "tesseract", "openai", "azure"];
const IMAGE_MODES = ["disabled", "auto", "always"];
const PDF_MODES = ["disabled", "auto", "always"];

export function OCRSettingsPanel({ settings }: OCRSettingsPanelProps) {
  const updateSettings = useUpdateOCRSettings();
  const form = useForm<OCRSettingsFormValues>({
    resolver: zodResolver(ocrSettingsSchema),
    defaultValues: {
      advanced_ocr_enabled: settings?.advanced_ocr_enabled ?? false,
      external_ocr_enabled: settings?.external_ocr_enabled ?? false,
      allow_document_content_to_external_ocr_provider:
        settings?.allow_document_content_to_external_ocr_provider ?? false,
      preferred_ocr_provider: settings?.preferred_ocr_provider ?? "local",
      preferred_ocr_model: settings?.preferred_ocr_model ?? "",
      image_ocr_mode: settings?.image_ocr_mode ?? "auto",
      scanned_pdf_ocr_mode: settings?.scanned_pdf_ocr_mode ?? "auto",
      max_scanned_pdf_pages: settings?.max_scanned_pdf_pages ?? 50,
      max_ocr_file_size_mb: settings?.max_ocr_file_size_mb ?? 25,
      max_ocr_chars_output: settings?.max_ocr_chars_output ?? 120_000,
      store_page_level_ocr: settings?.store_page_level_ocr ?? false,
      require_human_review: settings?.require_human_review ?? false,
    },
  });

  useEffect(() => {
    form.reset({
      advanced_ocr_enabled: settings?.advanced_ocr_enabled ?? false,
      external_ocr_enabled: settings?.external_ocr_enabled ?? false,
      allow_document_content_to_external_ocr_provider:
        settings?.allow_document_content_to_external_ocr_provider ?? false,
      preferred_ocr_provider: settings?.preferred_ocr_provider ?? "local",
      preferred_ocr_model: settings?.preferred_ocr_model ?? "",
      image_ocr_mode: settings?.image_ocr_mode ?? "auto",
      scanned_pdf_ocr_mode: settings?.scanned_pdf_ocr_mode ?? "auto",
      max_scanned_pdf_pages: settings?.max_scanned_pdf_pages ?? 50,
      max_ocr_file_size_mb: settings?.max_ocr_file_size_mb ?? 25,
      max_ocr_chars_output: settings?.max_ocr_chars_output ?? 120_000,
      store_page_level_ocr: settings?.store_page_level_ocr ?? false,
      require_human_review: settings?.require_human_review ?? false,
    });
  }, [form, settings]);

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="space-y-3">
        <CardTitle>Configuracoes de OCR</CardTitle>
        <div className="rounded-2xl border border-primary/20 bg-primary/5 p-3 text-sm text-muted-foreground">
          OCR externo continua desativado por padrao. O conteudo do documento nao sai do sistema
          sem opt-in explicito do tenant.
        </div>
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
              <span className="font-medium">Provider preferido</span>
              <Select
                value={form.watch("preferred_ocr_provider")}
                onValueChange={(value) => form.setValue("preferred_ocr_provider", value)}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Selecione um provider" />
                </SelectTrigger>
                <SelectContent>
                  {PROVIDERS.map((provider) => (
                    <SelectItem key={provider} value={provider}>
                      {provider}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-destructive">
                {form.formState.errors.preferred_ocr_provider?.message}
              </p>
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Modelo preferido</span>
              <Input {...form.register("preferred_ocr_model")} placeholder="Ex.: local-default" />
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Modo OCR de imagem</span>
              <Select
                value={form.watch("image_ocr_mode")}
                onValueChange={(value) => form.setValue("image_ocr_mode", value)}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Selecione o modo" />
                </SelectTrigger>
                <SelectContent>
                  {IMAGE_MODES.map((mode) => (
                    <SelectItem key={mode} value={mode}>
                      {mode}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-destructive">{form.formState.errors.image_ocr_mode?.message}</p>
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Modo OCR para PDF digitalizado</span>
              <Select
                value={form.watch("scanned_pdf_ocr_mode")}
                onValueChange={(value) => form.setValue("scanned_pdf_ocr_mode", value)}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Selecione o modo" />
                </SelectTrigger>
                <SelectContent>
                  {PDF_MODES.map((mode) => (
                    <SelectItem key={mode} value={mode}>
                      {mode}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-destructive">
                {form.formState.errors.scanned_pdf_ocr_mode?.message}
              </p>
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Maximo de paginas digitalizadas</span>
              <Input type="number" {...form.register("max_scanned_pdf_pages", { valueAsNumber: true })} />
            </label>
            <label className="space-y-2 text-sm">
              <span className="font-medium">Tamanho maximo do ficheiro (MB)</span>
              <Input type="number" {...form.register("max_ocr_file_size_mb", { valueAsNumber: true })} />
            </label>
            <label className="space-y-2 text-sm md:col-span-2">
              <span className="font-medium">Maximo de caracteres de saida</span>
              <Input type="number" {...form.register("max_ocr_chars_output", { valueAsNumber: true })} />
            </label>
          </div>

          <div className="grid gap-3 rounded-2xl border border-border/60 p-4 text-sm">
            {[
              ["advanced_ocr_enabled", "Permitir OCR avancado"],
              ["external_ocr_enabled", "Permitir providers externos de OCR"],
              [
                "allow_document_content_to_external_ocr_provider",
                "Permitir envio de conteudo do documento para OCR externo",
              ],
              ["store_page_level_ocr", "Armazenar OCR por pagina"],
              ["require_human_review", "Exigir revisao humana"],
            ].map(([fieldName, label]) => (
              <label key={fieldName} className="flex items-center gap-3">
                <input
                  type="checkbox"
                  className="size-4 rounded border-border"
                  checked={Boolean(form.watch(fieldName as keyof OCRSettingsFormValues))}
                  onChange={(event) =>
                    form.setValue(
                      fieldName as keyof OCRSettingsFormValues,
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
