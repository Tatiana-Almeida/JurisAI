"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { clearTokens, setTokens } from "@/lib/auth/tokens";
import type { AuthStatus, AuthTokens, User } from "@/types/auth";

type AuthState = {
  status: AuthStatus;
  user: User | null;
  tokens: AuthTokens | null;
  isBootstrapped: boolean;
  setAuthenticated: (payload: { user: User | null; tokens: AuthTokens }) => void;
  setUser: (user: User | null) => void;
  setLoading: () => void;
  markBootstrapped: () => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      status: "unauthenticated",
      user: null,
      tokens: null,
      isBootstrapped: false,
      setAuthenticated: ({ user, tokens }) => {
        setTokens(tokens);
        set({
          status: "authenticated",
          user,
          tokens,
          isBootstrapped: true,
        });
      },
      setUser: (user) =>
        set((state) => ({
          user,
          status: state.tokens?.access ? "authenticated" : "unauthenticated",
          isBootstrapped: true,
        })),
      setLoading: () => set({ status: "loading" }),
      markBootstrapped: () => set({ isBootstrapped: true }),
      logout: () => {
        clearTokens();
        set({
          status: "unauthenticated",
          user: null,
          tokens: null,
          isBootstrapped: true,
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
      onRehydrateStorage: () => (state) => {
        if (state) {
          state.isBootstrapped = false;
        }
      },
    },
  ),
);
