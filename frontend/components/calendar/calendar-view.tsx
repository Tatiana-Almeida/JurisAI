"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import listPlugin from "@fullcalendar/list";
import type { CalendarEvent } from "@/types/calendar";
import { EmptyState } from "@/components/shared/empty-state";

type CalendarViewProps = {
  events: CalendarEvent[];
};

function getEventColor(event: CalendarEvent) {
  if (event.status === "cancelled") {
    return "#94a3b8";
  }
  if (event.event_type === "deadline") {
    return "#ef4444";
  }
  if (event.event_type === "hearing") {
    return "#0284c7";
  }
  if (event.event_type === "financial") {
    return "#16a34a";
  }
  return "#1d4ed8";
}

export function CalendarView({ events }: CalendarViewProps) {
  if (events.length === 0) {
    return (
      <EmptyState
        title="Sem eventos"
        description="Os eventos de prazos, audiencias e compromissos desta organizacao aparecem aqui."
      />
    );
  }

  return (
    <div className="jurisai-panel rounded-3xl p-4">
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin, listPlugin]}
        initialView="dayGridMonth"
        headerToolbar={{
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,listWeek",
        }}
        height="auto"
        events={events.map((event) => ({
          id: event.id,
          title: event.title,
          start: event.start_at,
          end: event.end_at,
          color: getEventColor(event),
        }))}
      />
    </div>
  );
}
