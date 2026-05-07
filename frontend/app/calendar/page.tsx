"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { CalendarView } from "@/components/calendar/calendar-view";
import { EmptyState } from "@/components/shared/empty-state";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useCalendarEvents } from "@/hooks/use-calendar";

export default function CalendarPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const eventsQuery = useCalendarEvents({ ordering: "start_at" });

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar eventos, audiencias e compromissos."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Calendario"
          description="Calendario do tenant sobre `/api/v1/calendar/events/`, com cores por tipo e estado do evento."
        />
        {eventsQuery.isLoading ? <LoadingSkeleton /> : null}
        {eventsQuery.isError ? (
          <ErrorState
            title="Nao foi possivel carregar eventos"
            description="Confirme autenticacao, organizacao ativa e disponibilidade do modulo de calendario."
          />
        ) : null}
        {!eventsQuery.isLoading && !eventsQuery.isError ? <CalendarView events={eventsQuery.data ?? []} /> : null}
      </div>
    </AppShell>
  );
}
