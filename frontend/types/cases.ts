export interface LawCase {
  id: string;
  title: string;
  description?: string;
  status?: string;
  clientId?: string;
  lawyerId?: string;
  organizationId?: string;
  createdAt?: string;
}
