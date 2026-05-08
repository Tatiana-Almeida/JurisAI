export interface Organization {
  id: string;
  name: string;
  plan?: string;
  created_at?: string;
}

export interface OrganizationMembership {
  organizationId: string;
  role: string;
  organizationName?: string;
}
