"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { OrganizationSettings } from "@/components/settings/organization-settings";
import { OCRSettings } from "@/components/settings/ocr-settings";
import { ProfileSettings } from "@/components/settings/profile-settings";
import { RAGSettings } from "@/components/settings/rag-settings";
import { SecuritySettings } from "@/components/settings/security-settings";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useAuthStore } from "@/stores/auth-store";
import { useOCRSettings, useRAGSettings } from "@/hooks/use-jurisai-queries";

export default function SettingsPage() {
  const { activeOrganization } = useActiveOrganization();
  const user = useAuthStore((state) => state.user);
  const ocrSettingsQuery = useOCRSettings();
  const ragSettingsQuery = useRAGSettings();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Configurações"
          description="Painel base de conta, organização, OCR, RAG e segurança, sempre refletindo o estado real do backend."
        />
        <div className="grid gap-6 xl:grid-cols-2">
          <ProfileSettings user={user} />
          <OrganizationSettings organization={activeOrganization} />
          <OCRSettings settings={ocrSettingsQuery.data} />
          <RAGSettings settings={ragSettingsQuery.data} />
          <SecuritySettings />
        </div>
      </div>
    </AppShell>
  );
}
