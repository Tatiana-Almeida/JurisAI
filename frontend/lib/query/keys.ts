export type ScopedFilters = Record<string, string | number | boolean | undefined | null>;

export const queryKeys = {
  auth: () => ["auth"] as const,
  me: () => ["auth", "me"] as const,
  organizations: () => ["organizations"] as const,
  cases: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["cases", organizationId ?? "none", filters ?? {}] as const,
  caseDetail: (organizationId?: string | null, caseId?: string | null) =>
    ["case-detail", organizationId ?? "none", caseId ?? "none"] as const,
  clients: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["clients", organizationId ?? "none", filters ?? {}] as const,
  documents: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["documents", organizationId ?? "none", filters ?? {}] as const,
  documentDetail: (organizationId?: string | null, documentId?: string | null) =>
    ["document-detail", organizationId ?? "none", documentId ?? "none"] as const,
  ocrJobs: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["ocrJobs", organizationId ?? "none", filters ?? {}] as const,
  ocrResults: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["ocrResults", organizationId ?? "none", filters ?? {}] as const,
  ocrSettings: (organizationId?: string | null) =>
    ["ocrSettings", organizationId ?? "none"] as const,
  ocrAuditLogs: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["ocrAuditLogs", organizationId ?? "none", filters ?? {}] as const,
  pageResults: (organizationId?: string | null, resultId?: string | null) =>
    ["pageResults", organizationId ?? "none", resultId ?? "none"] as const,
  knowledgeBases: (organizationId?: string | null) =>
    ["knowledgeBases", organizationId ?? "none"] as const,
  knowledgeBaseDetail: (organizationId?: string | null, id?: string | null) =>
    ["knowledgeBaseDetail", organizationId ?? "none", id ?? "none"] as const,
  knowledgeDocuments: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["knowledgeDocuments", organizationId ?? "none", filters ?? {}] as const,
  indexingJobs: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["indexingJobs", organizationId ?? "none", filters ?? {}] as const,
  retrievalQueries: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["retrievalQueries", organizationId ?? "none", filters ?? {}] as const,
  ragSettings: (organizationId?: string | null) =>
    ["ragSettings", organizationId ?? "none"] as const,
  deadlines: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["deadlines", organizationId ?? "none", filters ?? {}] as const,
  calendarEvents: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["calendarEvents", organizationId ?? "none", filters ?? {}] as const,
  finance: (organizationId?: string | null) =>
    ["finance", organizationId ?? "none"] as const,
  financeInvoices: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["financeInvoices", organizationId ?? "none", filters ?? {}] as const,
  financeExpenses: (organizationId?: string | null, filters?: ScopedFilters) =>
    ["financeExpenses", organizationId ?? "none", filters ?? {}] as const,
  billing: (organizationId?: string | null) =>
    ["billing", organizationId ?? "none"] as const,
  clientPortal: (organizationId?: string | null) =>
    ["clientPortal", organizationId ?? "none"] as const,
  settings: (organizationId?: string | null) =>
    ["settings", organizationId ?? "none"] as const,
  dashboardSummary: (organizationId?: string | null) =>
    ["dashboardSummary", organizationId ?? "none"] as const,
  dashboardDeadlines: (organizationId?: string | null) =>
    ["dashboardDeadlines", organizationId ?? "none"] as const,
  dashboardDocuments: (organizationId?: string | null) =>
    ["dashboardDocuments", organizationId ?? "none"] as const,
  dashboardFinancial: (organizationId?: string | null) =>
    ["dashboardFinancial", organizationId ?? "none"] as const,
};

export const organizationScopedPrefixes = [
  "cases",
  "case-detail",
  "clients",
  "documents",
  "document-detail",
  "ocrJobs",
  "ocrResults",
  "ocrSettings",
  "ocrAuditLogs",
  "pageResults",
  "knowledgeBases",
  "knowledgeBaseDetail",
  "knowledgeDocuments",
  "indexingJobs",
  "retrievalQueries",
  "ragSettings",
  "deadlines",
  "calendarEvents",
  "finance",
  "financeInvoices",
  "financeExpenses",
  "billing",
  "clientPortal",
  "settings",
  "dashboardSummary",
  "dashboardDeadlines",
  "dashboardDocuments",
  "dashboardFinancial",
] as const;
