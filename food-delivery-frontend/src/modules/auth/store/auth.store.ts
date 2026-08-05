import { create } from "zustand";
import { persist } from "zustand/middleware";

import type { CurrentUser } from "../api/user.api";

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;

  user: CurrentUser | null;

  isAuthenticated: boolean;

  setTokens: (
    accessToken: string,
    refreshToken: string,
  ) => void;

  setUser: (
    user: CurrentUser,
  ) => void;

  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,

      user: null,

      isAuthenticated: false,

      setTokens: (
        accessToken,
        refreshToken,
      ) =>
        set({
          accessToken,
          refreshToken,
          isAuthenticated: true,
        }),

      setUser: (user) =>
        set({
          user,
        }),

      logout: () =>
        set({
          accessToken: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
        }),
    }),
    {
      name: "auth-storage",
    },
  ),
);