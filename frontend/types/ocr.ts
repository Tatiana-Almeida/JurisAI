export interface OCRJob {
  id: string;
  status: "pending" | "running" | "completed" | "failed" | "skipped";
  organization?: string;
  document?: string;
  requested_by?: string;
  extraction_method?: string;
  started_at?: string | null;
  finished_at?: string | null;
  error_message?: string;
  created_at?: string;
  updated_at?: string;
}

export interface OCRResult {
  id: string;
  organization?: string;
  job?: string;
  job_id?: string;
  document?: string;
  document_id?: string;
  extracted_text?: string;
  char_count?: number;
  metadata?: Record<string, unknown>;
  created_at?: string;
}

export interface OCRPageResult {
  id: string;
  organization?: string;
  ocr_result?: string;
  ocr_job?: string;
  document?: string;
  page_number: number;
  extracted_text?: string;
  char_count?: number;
  status?: string;
  error_message?: string;
  metadata?: Record<string, unknown>;
  created_at?: string;
}

export interface OCRSettings {
  organization?: string;
  advanced_ocr_enabled?: boolean;
  external_ocr_enabled?: boolean;
  allow_document_content_to_external_ocr_provider?: boolean;
  preferred_ocr_provider?: string;
  preferred_ocr_model?: string;
  image_ocr_mode?: string;
  scanned_pdf_ocr_mode?: string;
  max_scanned_pdf_pages?: number;
  max_ocr_file_size_mb?: number;
  max_ocr_chars_output?: number;
  store_page_level_ocr?: boolean;
  require_human_review?: boolean;
  updated_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface OCRAuditLog {
  id: string;
  organization?: string;
  document?: string;
  ocr_job?: string;
  action?: string;
  provider?: string;
  mode?: string;
  reason?: string;
  status?: string;
  metadata?: Record<string, unknown>;
  created_by?: string;
  created_at?: string;
}

export interface OCRKnowledgeBasePipelineRun {
  id: string;
  status: string;
  step?: string;
  document?: string;
  knowledge_base?: string;
  ocr_job?: string | null;
  ocr_result?: string | null;
  ocr_audit_log?: string | null;
  knowledge_document?: string | null;
  indexing_job?: string | null;
  used_advanced_ocr?: boolean;
  advanced_ocr_reason?: string;
  update_document_content?: boolean;
  error_message?: string;
  metadata?: Record<string, unknown>;
  created_by?: string;
  started_at?: string | null;
  finished_at?: string | null;
  created_at?: string;
  updated_at?: string;
}
