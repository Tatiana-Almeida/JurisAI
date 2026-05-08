"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { OrganizationSettings } from "@/components/settings/organization-settings";
import { OCRSettings } from "@/components/settings/ocr-settings";
import { ProfileSettings } from "@/components/settings/profile-settings";
import { RAGSettings } from "@/components/settings/rag-settings";
import { SecuritySettings } from "@/components/settings/security-settings";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useAuthStore } from "@/stores/auth-store";
import { useOCRSettings, useRAGSettings } from "@/hooks/use-jurisai-queries";

export default function SettingsPage() {
  const { activeOrganization, activeOrganizationId } = useActiveOrganization();
  const user = useAuthStore((state) => state.user);
  const ocrSettingsQuery = useOCRSettings();
  const ragSettingsQuery = useRAGSettings();

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar configuracoes de tenant, OCR e RAG."
        />
      </AppShell>
    );
  }

  if (ocrSettingsQuery.isLoading || ragSettingsQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (ocrSettingsQuery.isError || ragSettingsQuery.isError) {
    return (
      <AppShell>
        <ModuleErrorState
          moduleName="settings"
          description="Confirme autenticacao, organizacao ativa e acesso aos endpoints de settings do backend."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Configuracoes"
          description="Painel operacional de conta, organizacao, OCR, RAG e seguranca, sempre refletindo o estado real do backend."
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
