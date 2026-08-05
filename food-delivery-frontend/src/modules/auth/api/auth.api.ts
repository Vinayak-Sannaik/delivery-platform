import { apiClient } from "../../../shared/api/client";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export async function login(data: LoginRequest) {
  const response = await apiClient.post<LoginResponse>(
    "/auth/login",
    data
  );

  return response.data;
}