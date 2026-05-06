export interface KnowledgeBase {
  id: string;
  name: string;
  description?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface KnowledgeDocument {
  id: string;
  knowledge_base?: string;
  knowledge_base_id?: string;
  document?: string | null;
  document_id?: string | null;
  title: string;
  source_type?: string;
  status?: string;
  indexed_at?: string | null;
  error_message?: string;
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
}

export interface RetrievalSource {
  title?: string;
  excerpt?: string;
  final_score?: number;
  text_score?: number;
  embedding_score?: number;
  retrieval_method?: string;
  confidence?: string;
  fallback_used?: boolean;
  fallback_reason?: string;
}

export interface RetrievalQuery {
  id: string;
  knowledge_base?: string;
  created_by?: string;
  query: string;
  answer?: string;
  retrieval_method?: string;
  confidence?: string | null;
  sources_count?: number;
  sources_payload?: RetrievalSource[];
  status?: string;
  created_at?: string;
}

export interface IndexingJob {
  id: string;
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

export interface RAGSettings {
  retrieval_mode?: string;
  external_embeddings_enabled?: boolean;
  embedding_provider?: string;
  embedding_model?: string;
  require_human_review_for_ai_answers?: boolean;
  allow_document_content_to_external_provider?: boolean;
  max_sources_per_answer?: number;
  min_confidence_threshold?: string;
}

export interface EmbeddingAuditLog {
  id: string;
  chunk?: string;
  knowledge_document?: string;
  action?: string;
  status?: string;
  provider?: string;
  model?: string;
  reason?: string;
  metadata?: Record<string, unknown>;
  created_by?: string;
  created_at?: string;
}
