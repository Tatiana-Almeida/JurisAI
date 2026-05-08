"use client";

import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokens,
} from "@/lib/auth/tokens";
import { endpoints } from "@/lib/api/endpoints";
import type { ApiError } from "@/types/api";

type RetriableRequestConfig = InternalAxiosRequestConfig & {
  _retry?: boolean;
};

export function getApiBaseUrl() {
  return (
    process.env.NEXT_PUBLIC_API_URL?.trim() ||
    process.env.NEXT_PUBLIC_RENDER_API_URL?.trim() ||
    "http://localhost:8000"
  );
}

function toApiError(error: AxiosError<{ detail?: string }>): ApiError {
  const status = error.response?.status ?? 0;
  const hasResponse = Boolean(error.response);
  const message =
    error.response?.data?.detail ||
    (status === 401
      ? "Sessao expirada ou credenciais invalidas."
      : status === 402
        ? "A conta atual precisa de um plano elegivel para esta operacao."
        : status === 403
          ? "Voce nao tem permissao para aceder a este recurso."
          : status === 429
            ? "Muitas tentativas em pouco tempo. Tente novamente dentro de instantes."
            : status >= 500
              ? "O backend encontrou um erro interno. Tente novamente em instantes."
              : !hasResponse
                ? "Nao foi possivel contactar a API configurada."
                : error.message || "Ocorreu um erro inesperado.");

  return {
    status,
    message,
    detail: error.response?.data?.detail,
    data: error.response?.data,
    code: error.code,
  };
}

export const apiClient = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 20_000,
});

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<{ detail?: string }>) => {
    const status = error.response?.status;
    const refreshToken = getRefreshToken();
    const originalRequest = error.config as RetriableRequestConfig | undefined;

    if (
      status === 401 &&
      refreshToken &&
      originalRequest &&
      !originalRequest._retry &&
      originalRequest.url !== endpoints.auth.refresh
    ) {
      originalRequest._retry = true;

      try {
        const refreshResponse = await axios.post<{ access: string }>(
          `${getApiBaseUrl()}${endpoints.auth.refresh}`,
          { refresh: refreshToken },
          { timeout: 20_000 },
        );

        setTokens({
          access: refreshResponse.data.access,
          refresh: refreshToken,
        });

        originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
        return apiClient(originalRequest);
      } catch {
        clearTokens();
        if (typeof window !== "undefined") {
          window.dispatchEvent(new CustomEvent("jurisai:auth-expired"));
        }
        return Promise.reject(toApiError(error));
      }
    }

    if (status === 401) {
      clearTokens();
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("jurisai:auth-expired"));
      }
      return Promise.reject(toApiError(error));
    }

    if (status === 402 || status === 403 || status === 429 || status === 500) {
      return Promise.reject(toApiError(error));
    }

    return Promise.reject(toApiError(error));
  },
);

export function buildAuthHeader(token?: string | null) {
  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}

export { toApiError };
