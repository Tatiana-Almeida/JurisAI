export interface Client {
  id: string;
  name: string;
  email?: string;
  role?: "cliente" | "advogado" | "admin" | string;
  organization_id?: string;
  created_at?: string;
  updated_at?: string;
}
