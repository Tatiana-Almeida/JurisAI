import type { FieldValues, Path, UseFormSetError } from "react-hook-form";
import type { AxiosError } from "axios";
import type { DRFValidationError } from "@/types/api";

export function isDRFValidationError(error: unknown): error is AxiosError<DRFValidationError> {
  const candidate = error as AxiosError<DRFValidationError> | undefined;
  const data = candidate?.response?.data;

  return Boolean(
    data &&
      typeof data === "object" &&
      Object.values(data).some((value) => Array.isArray(value)),
  );
}

export function getNonFieldErrors(error: unknown): string[] {
  if (!isDRFValidationError(error)) {
    return [];
  }

  return error.response?.data?.non_field_errors ?? [];
}

export function getDRFErrorMessage(error: unknown) {
  if (isDRFValidationError(error)) {
    const nonField = getNonFieldErrors(error);
    if (nonField.length > 0) {
      return nonField.join(" ");
    }

    const firstField = Object.values(error.response?.data ?? {}).find((value) =>
      Array.isArray(value),
    );
    if (firstField) {
      return firstField.join(" ");
    }
  }

  const axiosError = error as AxiosError<{ detail?: string }> | undefined;
  return axiosError?.response?.data?.detail || "Nao foi possivel concluir a acao.";
}

export function mapDRFErrorsToForm<TFieldValues extends FieldValues>(
  error: unknown,
  setError: UseFormSetError<TFieldValues>,
) {
  if (!isDRFValidationError(error)) {
    return;
  }

  const payload = error.response?.data ?? {};

  Object.entries(payload).forEach(([field, messages]) => {
    if (!Array.isArray(messages) || messages.length === 0) {
      return;
    }

    if (field === "non_field_errors") {
      setError("root" as Path<TFieldValues>, {
        type: "server",
        message: messages.join(" "),
      });
      return;
    }

    setError(field as Path<TFieldValues>, {
      type: "server",
      message: messages.join(" "),
    });
  });
}
