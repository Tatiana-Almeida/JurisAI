import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function CalendarPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Calendário"
          description="FullCalendar já está instalado e a foundation do calendário pode começar no próximo passo."
        />
        <ModuleStateCard
          title="Calendar events"
          status="active"
          description="A UI final vai aproveitar FullCalendar com dados multi-tenant do backend."
          bullets={["Dependências instaladas.", "Estados base prontos para integração real."]}
        />
      </div>
    </AppShell>
  );
}
