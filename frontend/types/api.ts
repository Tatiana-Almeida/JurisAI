export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  status: number;
  message: string;
  detail?: string;
  data?: unknown;
}

export type DRFValidationError = Record<string, string[]>;

export interface HealthStatusResponse {
  status: string;
}
