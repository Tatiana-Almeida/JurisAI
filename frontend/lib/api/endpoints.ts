export const endpoints = {
  health: {
    public: "/health/",
    api: "/api/v1/health/",
  },
  auth: {
    login: "/api/v1/auth/token/",
    refresh: "/api/v1/auth/token/refresh/",
    verify: "/api/v1/auth/token/verify/",
    me: "/api/v1/users/profile/",
    users: "/api/v1/users/",
  },
  cases: {
    list: "/api/v1/cases/",
  },
  documents: {
    list: "/api/v1/documents/",
  },
  deadlines: {
    list: "/api/v1/deadlines/",
  },
  tasks: {
    list: "/api/v1/tasks/",
  },
  dashboard: {
    summary: "/api/v1/dashboard/summary/",
  },
  clientPortal: {
    cases: "/api/v1/client-portal/cases/",
    documents: "/api/v1/client-portal/documents/",
  },
  calendar: {
    events: "/api/v1/calendar/events/",
  },
  legalTemplates: {
    list: "/api/v1/legal-templates/",
    generated: "/api/v1/generated-documents/",
  },
  legalFinance: {
    summary: "/api/v1/legal-finance/summary/",
    invoices: "/api/v1/legal-finance/invoices/",
    payments: "/api/v1/legal-finance/payments/",
  },
  knowledgeBase: {
    list: "/api/v1/knowledge-base/",
    settings: "/api/v1/knowledge-base/settings/",
    documents: "/api/v1/knowledge-base/documents/",
    queries: "/api/v1/knowledge-base/queries/",
    indexingJobs: "/api/v1/knowledge-base/indexing-jobs/",
    embeddingAuditLogs: "/api/v1/knowledge-base/embedding-audit-logs/",
    chunks: "/api/v1/knowledge-base/chunks/",
  },
  ocr: {
    jobs: "/api/v1/ocr/jobs/",
    results: "/api/v1/ocr/results/",
    pageResults: "/api/v1/ocr/page-results/",
    pipelines: "/api/v1/ocr/pipelines/",
    settings: "/api/v1/ocr/settings/",
    auditLogs: "/api/v1/ocr/audit-logs/",
  },
  ai: {
    generatePetition: "/api/v1/ai/generate-petition/",
    summarizeDocument: "/api/v1/ai/summarize-document/",
    analyzeRisk: "/api/v1/ai/analyze-risk/",
    searchJurisprudence: "/api/v1/ai/search-jurisprudence/",
    draftContract: "/api/v1/ai/draft-contract/",
    reviewDocument: "/api/v1/ai/review-document/",
    history: "/api/v1/ai/history/",
  },
  billing: {
    payments: "/api/v1/payments/",
    subscriptions: "/api/v1/subscriptions/",
    invoices: "/api/v1/invoices/",
    webhook: "/api/v1/webhook/",
  },
} as const;
