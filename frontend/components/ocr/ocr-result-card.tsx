import type { OCRResult } from "@/types/ocr";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type OCRResultCardProps = {
  result: OCRResult;
  onApply?: () => void;
};

export function OCRResultCard({ result, onApply }: OCRResultCardProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Resultado OCR {result.id.slice(0, 8)}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground">Caracteres extraídos: {result.char_count ?? 0}</p>
        <div className="max-h-56 overflow-auto rounded-2xl border border-border/60 p-4 text-sm">
          {result.extracted_text?.slice(0, 1200) || "Sem texto extraído."}
        </div>
        <Button type="button" variant="outline" onClick={onApply}>
          Aplicar ao documento
        </Button>
      </CardContent>
    </Card>
  );
}
