import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { DashboardFoundation } from "@/components/shared/dashboard-foundation";

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Dashboard"
          description="Foundation dashboard para o Frontend MVP. Este ecrã ainda não representa a experiência final, mas já está pronto para ligar aos endpoints reais."
        />
        <DashboardFoundation />
      </div>
    </AppShell>
  );
}
