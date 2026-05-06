export interface OCRJob {
  id: string;
  status: "pending" | "running" | "completed" | "failed" | "skipped";
  documentId?: string;
  createdAt?: string;
}

export interface OCRResult {
  id: string;
  status?: string;
  extractedText?: string;
  charCount?: number;
  createdAt?: string;
}

export interface OCRPageResult {
  id: string;
  pageNumber: number;
  extractedText?: string;
  outputTruncated?: boolean;
}

export interface OCRSettings {
  externalOcrEnabled?: boolean;
  localImageOcrMode?: string;
  scannedPdfOcrMode?: string;
  maxScannedPdfPages?: number;
  maxOcrFileSizeMb?: number;
  maxOcrCharsOutput?: number;
}

export interface OCRAuditLog {
  id: string;
  provider?: string;
  mode?: string;
  reason?: string;
  status?: string;
  createdAt?: string;
}

export interface OCRKnowledgeBasePipelineRun {
  id: string;
  status: string;
  documentId?: string;
  knowledgeBaseId?: string;
}
