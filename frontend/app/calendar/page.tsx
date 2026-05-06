"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { CalendarView } from "@/components/calendar/calendar-view";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useCalendarEvents } from "@/hooks/use-jurisai-queries";

export default function CalendarPage() {
  const eventsQuery = useCalendarEvents();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Calendário"
          description="Calendário do tenant construído sobre FullCalendar e `/api/v1/calendar/events/`."
        />
        {eventsQuery.isLoading ? <LoadingSkeleton /> : null}
        {eventsQuery.isError ? (
          <ErrorState
            title="Não foi possível carregar eventos"
            description="Confirme autenticação e disponibilidade do módulo de calendário."
          />
        ) : null}
        {eventsQuery.data ? <CalendarView events={eventsQuery.data} /> : null}
      </div>
    </AppShell>
  );
}
