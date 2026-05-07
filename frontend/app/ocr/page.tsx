import { OCRPageClient } from "@/app/ocr/ocr-page-client";

type OCRPageProps = {
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
};

export default async function OCRPage({ searchParams }: OCRPageProps) {
  const resolvedSearchParams = (await searchParams) ?? {};
  const documentParam = resolvedSearchParams.document;
  const documentId = Array.isArray(documentParam) ? documentParam[0] : documentParam;

  return <OCRPageClient documentId={documentId} />;
}
