export interface Organization {
  id: string;
  name: string;
  plan?: string;
}

export interface OrganizationMembership {
  organizationId: string;
  role: string;
  organizationName?: string;
}
