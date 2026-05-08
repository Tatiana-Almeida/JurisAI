export interface KnowledgeBase {
  id: string;
  organization?: string;
  name: string;
  description?: string;
  is_active?: boolean;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface KnowledgeDocument {
  id: string;
  organization?: string;
  knowledge_base?: string;
  knowledge_base_id?: string;
  document?: string | null;
  document_id?: string | null;
  title: string;
  source_type?: string;
  status?: string;
  indexed_at?: string | null;
  error_message?: string;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface DocumentChunk {
  id: string;
  knowledge_document_id?: string;
  document_id?: string | null;
  chunk_index: number;
  content: string;
  content_hash?: string;
  metadata?: Record<string, unknown>;
  char_count?: number;
  embedding_status?: string;
  embedding?: string | null;
}

export interface SourceItem {
  title?: string;
  document_id?: string | null;
  knowledge_document_id?: string | null;
  excerpt?: string;
  chunk_index?: number;
  final_score?: number;
  text_score?: number;
  embedding_score?: number;
  retrieval_method?: string;
  confidence?: string | number | null;
  fallback_used?: boolean;
  fallback_reason?: string;
  metadata?: Record<string, unknown>;
}

export interface RetrievalSourcesPayload {
  retrieval_method?: string;
  effective_retrieval_mode?: string;
  fallback_used?: boolean;
  fallback_reason?: string;
  sources_count?: number;
  confidence?: string | number | null;
  sources?: SourceItem[];
}

export interface RetrievalQuery {
  id: string;
  organization?: string;
  knowledge_base?: string;
  created_by?: string;
  query: string;
  answer?: string;
  status?: string;
  retrieval_method?: string;
  confidence?: string | number | null;
  sources_count?: number;
  sources_payload?: RetrievalSourcesPayload;
  created_at?: string;
}

export interface SearchResponse {
  query: string;
  status?: string;
  retrieval_method?: string;
  effective_retrieval_mode?: string;
  fallback_used?: boolean;
  fallback_reason?: string;
  sources_count?: number;
  confidence?: string | number | null;
  sources?: SourceItem[];
}

export interface AskResponse extends SearchResponse {
  answer?: string;
}

export interface IndexingJob {
  id: string;
  organization?: string;
  knowledge_base?: string;
  knowledge_document?: string | null;
  document?: string | null;
  status: string;
  started_at?: string | null;
  finished_at?: string | null;
  chunks_created?: number;
  chunks_deleted?: number;
  error_message?: string;
  metadata?: Record<string, unknown>;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface KnowledgeBaseStats {
  total_documents?: number;
  indexed_documents?: number;
  failed_documents?: number;
  total_chunks?: number;
  last_indexed_at?: string | null;
  total_queries?: number;
  last_query_at?: string | null;
}

export interface RAGSettings {
  organization?: string;
  retrieval_mode?: string;
  external_embeddings_enabled?: boolean;
  embedding_provider?: string;
  embedding_model?: string;
  require_human_review_for_ai_answers?: boolean;
  allow_document_content_to_external_provider?: boolean;
  max_sources_per_answer?: number;
  min_confidence_threshold?: string;
  updated_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface EmbeddingAuditLog {
  id: string;
  chunk?: string;
  knowledge_document?: string;
  provider?: string;
  model?: string;
  action?: string;
  status?: string;
  reason?: string;
  metadata?: Record<string, unknown>;
  created_by?: string;
  created_at?: string;
}

export interface PrepareEmbeddingsResponse {
  status: string;
  reason?: string;
  provider?: string;
  model?: string;
  chunks_processed?: number;
  embeddings_created?: number;
  embeddings_skipped?: number;
  audit_log_id?: string | null;
  effective_retrieval_mode?: string;
}
