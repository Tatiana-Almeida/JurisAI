"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { clearTokens, setTokens } from "@/lib/auth/tokens";
import type { AuthStatus, AuthTokens, User } from "@/types/auth";

type AuthState = {
  status: AuthStatus;
  user: User | null;
  tokens: AuthTokens | null;
  setAuthenticated: (payload: { user: User | null; tokens: AuthTokens }) => void;
  setLoading: () => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      status: "unauthenticated",
      user: null,
      tokens: null,
      setAuthenticated: ({ user, tokens }) => {
        setTokens(tokens);
        set({
          status: "authenticated",
          user,
          tokens,
        });
      },
      setLoading: () => set({ status: "loading" }),
      logout: () => {
        clearTokens();
        set({
          status: "unauthenticated",
          user: null,
          tokens: null,
        });
      },
    }),
    {
      name: "jurisai.auth-store",
      partialize: (state) => ({
        status: state.status === "authenticated" ? state.status : "unauthenticated",
        user: state.user,
        tokens: state.tokens,
      }),
    },
  ),
);
