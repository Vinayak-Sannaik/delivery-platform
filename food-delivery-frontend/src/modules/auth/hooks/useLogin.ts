import { useMutation } from "@tanstack/react-query";

import {
  login,
  type LoginRequest,
  type LoginResponse,
} from "../api/auth.api";
import { getCurrentUser } from "../api/user.api";
import { useAuthStore } from "../store/auth.store";

import { apiClient } from "../../../shared/api/client";

export function useLogin() {
  const setTokens = useAuthStore((state) => state.setTokens);
  const setUser = useAuthStore((state) => state.setUser);

  return useMutation<LoginResponse, Error, LoginRequest>({
    mutationFn: async (credentials) => {
      const response = await login(credentials);

      setTokens(
        response.access_token,
        response.refresh_token,
      );

      apiClient.defaults.headers.common.Authorization =
        `Bearer ${response.access_token}`;

      const user = await getCurrentUser();

      setUser(user);

      return response;
    },
  });
}