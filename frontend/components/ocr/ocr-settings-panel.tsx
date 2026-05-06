import type { OCRSettings } from "@/types/ocr";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type OCRSettingsPanelProps = {
  settings?: OCRSettings;
};

export function OCRSettingsPanel({ settings }: OCRSettingsPanelProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>OCR settings</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-3 text-sm text-muted-foreground md:grid-cols-2">
        <div>advanced_ocr_enabled: {String(settings?.advanced_ocr_enabled ?? false)}</div>
        <div>external_ocr_enabled: {String(settings?.external_ocr_enabled ?? false)}</div>
        <div>max_scanned_pdf_pages: {settings?.max_scanned_pdf_pages ?? "—"}</div>
        <div>max_ocr_file_size_mb: {settings?.max_ocr_file_size_mb ?? "—"}</div>
        <div>max_ocr_chars_output: {settings?.max_ocr_chars_output ?? "—"}</div>
        <div>store_page_level_ocr: {String(settings?.store_page_level_ocr ?? false)}</div>
      </CardContent>
    </Card>
  );
}
