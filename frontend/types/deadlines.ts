export interface Deadline {
  id: string;
  law_case?: string;
  law_case_id?: string;
  due_date?: string;
  completed?: boolean;
  organization_id?: string;
  created_at?: string;
  updated_at?: string;
  days_remaining?: number;
  is_overdue?: boolean;
}
