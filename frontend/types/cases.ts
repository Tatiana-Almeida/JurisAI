import type { User } from "@/types/auth";

export interface LawCase {
  id: string;
  title: string;
  description?: string;
  status?: "open" | "in_progress" | "closed" | "on_hold" | string;
  client?: User | null;
  lawyer?: User | null;
  client_id?: string;
  lawyer_id?: string;
  organization_id?: string;
  created_at?: string;
  updated_at?: string;
  deleted?: boolean;
}
