"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { clearTokens, setTokens } from "@/lib/auth/tokens";
import { queryClient } from "@/lib/query/query-client";
import { useOrganizationStore } from "@/stores/organization-store";
import type { AuthStatus, AuthTokens, User } from "@/types/auth";

type AuthState = {
  status: AuthStatus;
  user: User | null;
  tokens: AuthTokens | null;
  isBootstrapped: boolean;
  bootstrapAuth: () => void;
  setAuthenticated: (payload: { user: User | null; tokens: AuthTokens }) => void;
  setUser: (user: User | null) => void;
  setTokens: (tokens: AuthTokens | null) => void;
  setLoading: () => void;
  markBootstrapped: () => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      status: "idle",
      user: null,
      tokens: null,
      isBootstrapped: false,
      bootstrapAuth: () =>
        set((state) => ({
          status: state.tokens?.access ? "loading" : "unauthenticated",
          isBootstrapped: false,
        })),
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
      setTokens: (tokens) =>
        set((state) => ({
          tokens,
          status: tokens?.access ? state.status : "unauthenticated",
        })),
      setLoading: () => set({ status: "loading" }),
      markBootstrapped: () => set({ isBootstrapped: true }),
      logout: () => {
        clearTokens();
        queryClient.clear();
        useOrganizationStore.getState().reset();
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
        status: state.status === "authenticated" ? state.status : "idle",
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
