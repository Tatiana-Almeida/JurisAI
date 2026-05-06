"use client";

import { useMemo } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { apiClient } from "@/lib/api/client";
import { endpoints } from "@/lib/api/endpoints";
import { buildPaginatedParams, extractResults, type PaginatedPayload } from "@/lib/api/pagination";
import { queryKeys } from "@/lib/query/keys";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import type { HealthStatusResponse, PaginatedResponse } from "@/types/api";
import type { LawCase } from "@/types/cases";
import type { Client } from "@/types/clients";
import type { CalendarEvent } from "@/types/calendar";
import type { Deadline } from "@/types/deadlines";
import type { Document } from "@/types/documents";
import type { FinanceSummary, Invoice, Expense } from "@/types/finance";
import type {
  EmbeddingAuditLog,
  IndexingJob,
  KnowledgeBase,
  KnowledgeDocument,
  RAGSettings,
  RetrievalQuery,
} from "@/types/knowledge-base";
import type {
  OCRAuditLog,
  OCRJob,
  OCRKnowledgeBasePipelineRun,
  OCRPageResult,
  OCRResult,
  OCRSettings,
} from "@/types/ocr";
import type { BillingInvoice, BillingSubscription } from "@/types/billing";
import type { User } from "@/types/auth";

type ListParams = Record<string, string | number | boolean | undefined | null>;

async function getList<T>(
  path: string,
  params?: ListParams,
): Promise<PaginatedPayload<T> | T[]> {
  const response = await apiClient.get<PaginatedPayload<T> | T[]>(path, {
    params: buildPaginatedParams(params ?? {}),
  });
  return response.data;
}

function useTenantContext() {
  const queryClient = useQueryClient();
  const { activeOrganization, activeOrganizationId } = useActiveOrganization();
  return {
    queryClient,
    activeOrganization,
    activeOrganizationId,
  };
}

export function useHealthStatus() {
  return useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await apiClient.get<HealthStatusResponse>(endpoints.health.api);
      return response.data;
    },
    retry: 1,
  });
}

export function useDashboardSummary() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.dashboardSummary(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<{
        total_cases: number;
        active_cases: number;
        total_documents: number;
        upcoming_deadlines: number;
        overdue_deadlines: number;
        pending_tasks: number;
        completed_tasks: number;
        pending_invoices: number;
      }>(endpoints.dashboard.summary);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useDashboardDeadlines() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.dashboardDeadlines(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<Deadline[]>(endpoints.dashboard.deadlines);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useDashboardDocuments() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.dashboardDocuments(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<Document[]>(endpoints.dashboard.documents);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useDashboardFinancial() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.dashboardFinancial(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<{
        pending_invoices: number;
        paid_invoices: number;
        overdue_invoices: number;
      }>(endpoints.dashboard.financial);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useCases(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.cases(activeOrganizationId, filters),
    queryFn: async () => extractResults<LawCase>(await getList<LawCase>(endpoints.cases.list, filters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useCase(caseId?: string) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.caseDetail(activeOrganizationId, caseId),
    queryFn: async () => {
      const response = await apiClient.get<LawCase>(endpoints.cases.detail(caseId!));
      return response.data;
    },
    enabled: Boolean(activeOrganizationId && caseId),
  });
}

export function useClients(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  const mergedFilters = useMemo(() => ({ role: "cliente", ...(filters ?? {}) }), [filters]);
  return useQuery({
    queryKey: queryKeys.clients(activeOrganizationId, mergedFilters),
    queryFn: async () => extractResults<Client>(await getList<Client>(endpoints.clients.list, mergedFilters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useLawyers() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: ["lawyers", activeOrganizationId ?? "none"],
    queryFn: async () =>
      extractResults<User>(
        await getList<User>(endpoints.auth.users, {
          role: "advogado",
        }),
      ),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useDocuments(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.documents(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<Document>(await getList<Document>(endpoints.documents.list, filters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useDocument(documentId?: string) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.documentDetail(activeOrganizationId, documentId),
    queryFn: async () => {
      const response = await apiClient.get<Document>(endpoints.documents.detail(documentId!));
      return response.data;
    },
    enabled: Boolean(activeOrganizationId && documentId),
  });
}

export function useOCRJobs(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.ocrJobs(activeOrganizationId, filters),
    queryFn: async () => extractResults<OCRJob>(await getList<OCRJob>(endpoints.ocr.jobs, filters)),
    enabled: Boolean(activeOrganizationId),
    refetchInterval: (query) => {
      const rows = query.state.data as OCRJob[] | undefined;
      return rows?.some((job) => job.status === "pending" || job.status === "running")
        ? 5000
        : false;
    },
  });
}

export function useOCRResults(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.ocrResults(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<OCRResult>(await getList<OCRResult>(endpoints.ocr.results, filters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useOCRSettings() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.ocrSettings(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<OCRSettings>(endpoints.ocr.settings);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useOCRAuditLogs(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.ocrAuditLogs(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<OCRAuditLog>(
        await getList<OCRAuditLog>(endpoints.ocr.auditLogs, filters),
      ),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useOCRPageResults(resultId?: string) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.pageResults(activeOrganizationId, resultId),
    queryFn: async () => {
      if (!resultId) {
        return [] as OCRPageResult[];
      }
      const response = await apiClient.get<PaginatedResponse<OCRPageResult> | OCRPageResult[]>(
        endpoints.ocr.resultPages(resultId),
      );
      return extractResults(response.data);
    },
    enabled: Boolean(activeOrganizationId && resultId),
  });
}

export function useOCRPipelines(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: ["ocrPipelines", activeOrganizationId ?? "none", filters ?? {}],
    queryFn: async () =>
      extractResults<OCRKnowledgeBasePipelineRun>(
        await getList<OCRKnowledgeBasePipelineRun>(endpoints.ocr.pipelines, filters),
      ),
    enabled: Boolean(activeOrganizationId),
    refetchInterval: (query) => {
      const rows = query.state.data as OCRKnowledgeBasePipelineRun[] | undefined;
      return rows?.some((item) => item.status === "pending" || item.status === "running")
        ? 5000
        : false;
    },
  });
}

export function useKnowledgeBases() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.knowledgeBases(activeOrganizationId),
    queryFn: async () => extractResults<KnowledgeBase>(await getList<KnowledgeBase>(endpoints.knowledgeBase.list)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useKnowledgeBase(id?: string) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.knowledgeBaseDetail(activeOrganizationId, id),
    queryFn: async () => {
      const response = await apiClient.get<KnowledgeBase>(endpoints.knowledgeBase.detail(id!));
      return response.data;
    },
    enabled: Boolean(activeOrganizationId && id),
  });
}

export function useKnowledgeDocuments(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.knowledgeDocuments(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<KnowledgeDocument>(
        await getList<KnowledgeDocument>(endpoints.knowledgeBase.documents, filters),
      ),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useIndexingJobs(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.indexingJobs(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<IndexingJob>(
        await getList<IndexingJob>(endpoints.knowledgeBase.indexingJobs, filters),
      ),
    enabled: Boolean(activeOrganizationId),
    refetchInterval: (query) => {
      const rows = query.state.data as IndexingJob[] | undefined;
      return rows?.some((item) => item.status === "pending" || item.status === "running")
        ? 5000
        : false;
    },
  });
}

export function useRetrievalQueries(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.retrievalQueries(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<RetrievalQuery>(
        await getList<RetrievalQuery>(endpoints.knowledgeBase.queries, filters),
      ),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useRAGSettings() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.ragSettings(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<RAGSettings>(endpoints.knowledgeBase.settings);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useEmbeddingAuditLogs(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: ["embeddingAuditLogs", activeOrganizationId ?? "none", filters ?? {}],
    queryFn: async () =>
      extractResults<EmbeddingAuditLog>(
        await getList<EmbeddingAuditLog>(
          endpoints.knowledgeBase.embeddingAuditLogs,
          filters,
        ),
      ),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useDeadlines(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.deadlines(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<Deadline>(await getList<Deadline>(endpoints.deadlines.list, filters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useCalendarEvents(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.calendarEvents(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<CalendarEvent>(
        await getList<CalendarEvent>(endpoints.calendar.events, filters),
      ),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useFinanceSummary() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.finance(activeOrganizationId),
    queryFn: async () => {
      const response = await apiClient.get<FinanceSummary>(endpoints.legalFinance.summary);
      return response.data;
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useFinanceInvoices(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.financeInvoices(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<Invoice>(await getList<Invoice>(endpoints.legalFinance.invoices, filters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useFinanceExpenses(filters?: ListParams) {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.financeExpenses(activeOrganizationId, filters),
    queryFn: async () =>
      extractResults<Expense>(await getList<Expense>(endpoints.legalFinance.expenses, filters)),
    enabled: Boolean(activeOrganizationId),
  });
}

export function useBillingSummary() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.billing(activeOrganizationId),
    queryFn: async () => {
      const [subscriptionsResponse, invoicesResponse] = await Promise.all([
        getList<BillingSubscription>(endpoints.billing.subscriptions),
        getList<BillingInvoice>(endpoints.billing.invoices),
      ]);

      return {
        subscriptions: extractResults(subscriptionsResponse),
        invoices: extractResults(invoicesResponse),
      };
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useClientPortalData() {
  const { activeOrganizationId } = useTenantContext();
  return useQuery({
    queryKey: queryKeys.clientPortal(activeOrganizationId),
    queryFn: async () => {
      const [casesResponse, documentsResponse, messagesResponse] = await Promise.all([
        apiClient.get<LawCase[]>(endpoints.clientPortal.cases),
        apiClient.get<Document[]>(endpoints.clientPortal.documents),
        apiClient.get(endpoints.clientPortal.messages),
      ]);

      return {
        cases: casesResponse.data,
        documents: documentsResponse.data,
        messages: messagesResponse.data as Array<Record<string, unknown>>,
      };
    },
    enabled: Boolean(activeOrganizationId),
  });
}

export function useCreateCase() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (payload: Record<string, unknown>) => {
      const response = await apiClient.post<LawCase>(endpoints.cases.list, payload);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.cases(activeOrganizationId) });
      toast.success("Processo criado com sucesso.");
    },
  });
}

export function useUpdateCase(caseId?: string) {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (payload: Record<string, unknown>) => {
      const response = await apiClient.patch<LawCase>(endpoints.cases.detail(caseId!), payload);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.cases(activeOrganizationId) });
      queryClient.invalidateQueries({
        queryKey: queryKeys.caseDetail(activeOrganizationId, caseId),
      });
      toast.success("Processo atualizado com sucesso.");
    },
  });
}

export function useCreateClient() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (payload: Record<string, unknown>) => {
      const response = await apiClient.post<Client>(endpoints.clients.list, payload);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.clients(activeOrganizationId) });
      toast.success("Cliente criado com sucesso.");
    },
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (payload: {
      formData: FormData;
      onUploadProgress?: (progressEvent: {
        loaded: number;
        total?: number;
      }) => void;
    }) => {
      const response = await apiClient.post<Document>(endpoints.documents.list, payload.formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: payload.onUploadProgress,
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.documents(activeOrganizationId) });
      toast.success("Documento enviado com sucesso.");
    },
  });
}

export function useRunOCR() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (documentId: string) => {
      const response = await apiClient.post(endpoints.ocr.runDocument(documentId), {
        update_document_content: false,
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.ocrJobs(activeOrganizationId) });
      queryClient.invalidateQueries({ queryKey: queryKeys.ocrResults(activeOrganizationId) });
      toast.success("OCR iniciado.");
    },
  });
}

export function useRunAdvancedOCR() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (documentId: string) => {
      const response = await apiClient.post(endpoints.ocr.runAdvancedDocument(documentId), {
        update_document_content: false,
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.ocrJobs(activeOrganizationId) });
      queryClient.invalidateQueries({ queryKey: queryKeys.ocrResults(activeOrganizationId) });
      toast.success("OCR avançado iniciado.");
    },
  });
}

export function useApplyOCRResult() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (resultId: string) => {
      const response = await apiClient.post(endpoints.ocr.applyResult(resultId), {});
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.documents(activeOrganizationId) });
      queryClient.invalidateQueries({ queryKey: queryKeys.ocrResults(activeOrganizationId) });
      toast.success("Resultado de OCR aplicado ao documento.");
    },
  });
}

export function useCreateKnowledgeBase() {
  const queryClient = useQueryClient();
  const { activeOrganizationId } = useTenantContext();
  return useMutation({
    mutationFn: async (payload: Record<string, unknown>) => {
      const response = await apiClient.post<KnowledgeBase>(endpoints.knowledgeBase.list, payload);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.knowledgeBases(activeOrganizationId),
      });
      toast.success("Knowledge Base criada.");
    },
  });
}

export function useAskKnowledgeBase(knowledgeBaseId?: string) {
  return useMutation({
    mutationFn: async (payload: { query: string; limit?: number }) => {
      const response = await apiClient.post(endpoints.knowledgeBase.ask(knowledgeBaseId!), payload);
      return response.data as {
        answer?: string;
        confidence?: string;
        sources_count?: number;
        retrieval_method?: string;
        sources?: Array<Record<string, unknown>>;
        fallback_used?: boolean;
        fallback_reason?: string;
      };
    },
  });
}
