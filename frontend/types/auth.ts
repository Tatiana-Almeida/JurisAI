import type { Organization, OrganizationMembership } from "@/types/organization";

export interface User {
  id?: string;
  email: string;
  name?: string;
  role?: "admin" | "advogado" | "cliente" | string;
  organization?: Organization | null;
  organization_id?: string;
  created_at?: string;
  updated_at?: string;
  memberships?: OrganizationMembership[];
}

export interface AuthTokens {
  access: string;
  refresh?: string;
}

export type AuthStatus = "idle" | "loading" | "authenticated" | "unauthenticated";
