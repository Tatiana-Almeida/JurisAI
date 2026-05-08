import type { AuthTokens } from "@/types/auth";

const ACCESS_TOKEN_KEY = "jurisai.access-token";
const REFRESH_TOKEN_KEY = "jurisai.refresh-token";
const SESSION_HINT_COOKIE = "jurisai-has-session";

function isBrowser() {
  return typeof window !== "undefined";
}

export function getAccessToken() {
  if (!isBrowser()) {
    return null;
  }

  return window.localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
  if (!isBrowser()) {
    return null;
  }

  return window.localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setTokens(tokens: AuthTokens) {
  if (!isBrowser()) {
    return;
  }

  window.localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
  if (tokens.refresh) {
    window.localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
  }
  document.cookie = `${SESSION_HINT_COOKIE}=1; path=/; SameSite=Lax${
    window.location.protocol === "https:" ? "; Secure" : ""
  }`;
}

export function clearTokens() {
  if (!isBrowser()) {
    return;
  }

  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(REFRESH_TOKEN_KEY);
  document.cookie = `${SESSION_HINT_COOKIE}=; Max-Age=0; path=/; SameSite=Lax${
    window.location.protocol === "https:" ? "; Secure" : ""
  }`;
}

export const TOKEN_STORAGE_KEYS = {
  ACCESS_TOKEN_KEY,
  REFRESH_TOKEN_KEY,
  SESSION_HINT_COOKIE,
};
