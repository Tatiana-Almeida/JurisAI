"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import listPlugin from "@fullcalendar/list";
import type { CalendarEvent } from "@/types/calendar";

type CalendarViewProps = {
  events: CalendarEvent[];
};

export function CalendarView({ events }: CalendarViewProps) {
  return (
    <div className="jurisai-panel rounded-3xl p-4">
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin, listPlugin]}
        initialView="dayGridMonth"
        height="auto"
        events={events.map((event) => ({
          id: event.id,
          title: event.title,
          start: event.start_at,
          end: event.end_at,
        }))}
      />
    </div>
  );
}
