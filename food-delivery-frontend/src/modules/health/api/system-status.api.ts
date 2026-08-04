import { apiClient } from "../../../shared/api/client";

export interface ServiceStatus {
  name: string;
  status: string;
  latency_ms: number | null;
}

export interface SystemStatusResponse {
  ready: boolean;
  services: ServiceStatus[];
}


export async function getSystemStatus(): Promise<SystemStatusResponse> {
  const { data } = await apiClient.get<SystemStatusResponse>(
    "/system/status"
  );

  return data;
}