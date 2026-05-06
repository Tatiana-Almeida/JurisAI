import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { DocumentUploadDropzone } from "@/components/documents/document-upload-dropzone";

export default function DocumentsPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Documentos"
          description="Foundation para documentos, uploads seguros e integração posterior com OCR e Knowledge Base."
        />
        <DocumentUploadDropzone />
      </div>
    </AppShell>
  );
}
