export const queryKeys = {
  auth: () => ["auth"] as const,
  me: () => ["auth", "me"] as const,
  organizations: () => ["organizations"] as const,
  cases: (organizationId?: string | null) =>
    ["cases", organizationId ?? "none"] as const,
  clients: (organizationId?: string | null) =>
    ["clients", organizationId ?? "none"] as const,
  documents: (organizationId?: string | null) =>
    ["documents", organizationId ?? "none"] as const,
  ocrJobs: (organizationId?: string | null) =>
    ["ocrJobs", organizationId ?? "none"] as const,
  ocrResults: (organizationId?: string | null) =>
    ["ocrResults", organizationId ?? "none"] as const,
  knowledgeBases: (organizationId?: string | null) =>
    ["knowledgeBases", organizationId ?? "none"] as const,
  indexingJobs: (organizationId?: string | null) =>
    ["indexingJobs", organizationId ?? "none"] as const,
  deadlines: (organizationId?: string | null) =>
    ["deadlines", organizationId ?? "none"] as const,
  calendarEvents: (organizationId?: string | null) =>
    ["calendarEvents", organizationId ?? "none"] as const,
  finance: (organizationId?: string | null) =>
    ["finance", organizationId ?? "none"] as const,
  billing: (organizationId?: string | null) =>
    ["billing", organizationId ?? "none"] as const,
  settings: (organizationId?: string | null) =>
    ["settings", organizationId ?? "none"] as const,
};

export const organizationScopedPrefixes = [
  "cases",
  "clients",
  "documents",
  "ocrJobs",
  "ocrResults",
  "knowledgeBases",
  "indexingJobs",
  "deadlines",
  "calendarEvents",
  "finance",
  "billing",
  "settings",
] as const;
