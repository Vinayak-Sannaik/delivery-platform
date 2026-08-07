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

export type SignupRole =
  | "CUSTOMER"
  | "RESTAURANT_OWNER";

export interface SignupRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone: string;
  role: SignupRole;
}

export interface SignupResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: SignupRole;
}

export async function signup(
  data: SignupRequest,
): Promise<SignupResponse> {
  const response = await apiClient.post<SignupResponse>(
    "/auth/signup",
    data,
  );

  return response.data;
}

export async function login(data: LoginRequest) {
  const response = await apiClient.post<LoginResponse>(
    "/auth/login",
    data
  );

  return response.data;
}