export interface KnowledgeBase {
  id: string;
  name: string;
  description?: string;
  isActive?: boolean;
}

export interface KnowledgeDocument {
  id: string;
  knowledgeBaseId?: string;
  documentId?: string;
  title: string;
  status?: string;
  indexedAt?: string;
}

export interface DocumentChunk {
  id: string;
  chunkIndex: number;
  content: string;
  documentId?: string;
}

export interface RetrievalSource {
  title: string;
  excerpt: string;
  final_score?: number;
  text_score?: number;
  embedding_score?: number;
}

export interface RetrievalQuery {
  id: string;
  query: string;
  answer?: string;
  retrieval_method?: string;
  confidence?: string | null;
  sources_count?: number;
}

export interface IndexingJob {
  id: string;
  status: string;
  chunksCreated?: number;
  chunksDeleted?: number;
  createdAt?: string;
}

export interface RAGSettings {
  retrieval_mode?: string;
  embedding_provider?: string;
  embedding_model?: string;
  max_sources_per_answer?: number;
  min_confidence_threshold?: string;
  external_embeddings_enabled?: boolean;
  allow_document_content_to_external_provider?: boolean;
}

export interface EmbeddingAuditLog {
  id: string;
  action?: string;
  status?: string;
  provider?: string;
  model?: string;
  reason?: string;
}
