import { apiClient } from "../../../shared/api/client";

export interface CurrentUser {
  id: string;
  email: string;
  role: string;
}

export async function getCurrentUser() {
  const { data } = await apiClient.get<CurrentUser>(
    "/auth/me"
  );

  return data;
}