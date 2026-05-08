import type { PaginatedResponse } from "@/types/api";

export type PaginatedPayload<T> = PaginatedResponse<T> | T[];

export function isPaginatedResponse<T>(value: unknown): value is PaginatedResponse<T> {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Partial<PaginatedResponse<T>>;
  return (
    typeof candidate.count === "number" &&
    "results" in candidate &&
    Array.isArray(candidate.results)
  );
}

export function extractResults<T>(value: PaginatedPayload<T>): T[] {
  if (Array.isArray(value)) {
    return value;
  }

  return value.results;
}

export function buildPaginatedParams(
  params: Record<string, string | number | boolean | null | undefined>,
) {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== ""),
  );
}
