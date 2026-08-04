import { apiClient } from "../../../shared/api/client";
import { API } from "../../../shared/api/endpoints";
import type { HealthResponse } from "../types";

export async function getHealth(): Promise<HealthResponse> {
  const response = await apiClient.get<HealthResponse>(API.HEALTH);

  return response.data;
}