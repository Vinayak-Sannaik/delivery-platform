import { apiClient } from "../../../shared/api/client";
import { API } from "../../../shared/api/endpoints";

import type {
  LoginRequest,
  LoginResponse,
} from "../types";

export async function login(
  payload: LoginRequest
): Promise<LoginResponse> {
  const { data } = await apiClient.post<LoginResponse>(
    API.LOGIN,
    payload
  );

  return data;
}