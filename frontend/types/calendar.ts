export interface CalendarEvent {
  id: string;
  title: string;
  organization_id?: string;
  law_case_id?: string | null;
  assigned_to_id?: string | null;
  start_at?: string;
  end_at?: string;
  event_type?: string;
  location?: string;
  status?: string;
  description?: string;
}
