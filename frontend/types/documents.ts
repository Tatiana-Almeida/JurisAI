export interface Document {
  id: string;
  law_case?: string | null;
  law_case_id?: string;
  type?: "petition" | "contract" | "evidence" | "internal" | string;
  file?: string | null;
  content?: string;
  version?: number;
  organization_id?: string;
  created_at?: string;
  updated_at?: string;
}
