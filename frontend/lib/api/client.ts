"use client";

import axios, { AxiosError } from "axios";
import { clearTokens, getAccessToken } from "@/lib/auth/tokens";
import type { ApiError } from "@/types/api";

export function getApiBaseUrl() {
  return (
    process.env.NEXT_PUBLIC_API_URL?.trim() ||
    process.env.NEXT_PUBLIC_RENDER_API_URL?.trim() ||
    "http://localhost:8000"
  );
}

function toApiError(error: AxiosError<{ detail?: string }>): ApiError {
  return {
    status: error.response?.status ?? 500,
    message:
      error.response?.data?.detail ||
      error.message ||
      "Ocorreu um erro inesperado.",
    detail: error.response?.data?.detail,
    data: error.response?.data,
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

    if (status === 401) {
      clearTokens();
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("jurisai:auth-expired"));
      }
    }

    if (status === 402 || status === 403 || status === 429 || status === 500) {
      return Promise.reject(toApiError(error));
    }

    return Promise.reject(error);
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
