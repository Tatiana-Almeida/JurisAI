import type { Organization, OrganizationMembership } from "@/types/organization";

export interface User {
  id?: string;
  email: string;
  name?: string;
  role?: string;
  organization?: Organization | null;
  memberships?: OrganizationMembership[];
}

export interface AuthTokens {
  access: string;
  refresh?: string;
}

export type AuthStatus = "loading" | "authenticated" | "unauthenticated";
