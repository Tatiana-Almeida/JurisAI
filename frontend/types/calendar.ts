export type CalendarEventType =
  | "deadline"
  | "hearing"
  | "meeting"
  | "task"
  | "financial"
  | "custom"
  | string;

export type CalendarEventStatus = "scheduled" | "completed" | "cancelled" | string;

export interface CalendarEvent {
  id: string;
  title: string;
  organization_id?: string;
  law_case_id?: string | null;
  assigned_to_id?: string | null;
  created_by_id?: string | null;
  start_at?: string;
  end_at?: string;
  event_type?: CalendarEventType;
  location?: string;
  status?: CalendarEventStatus;
  description?: string;
}
