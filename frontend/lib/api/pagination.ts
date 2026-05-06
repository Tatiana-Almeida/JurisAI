import type { PaginatedResponse } from "@/types/api";

export function isPaginatedResponse<T>(
  value: unknown,
): value is PaginatedResponse<T> {
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
