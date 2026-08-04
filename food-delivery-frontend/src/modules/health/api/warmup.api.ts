import { apiClient } from "../../../shared/api/client";

import type { SystemStatusResponse } from "./system-status.api";


export async function warmupServices(): Promise<SystemStatusResponse> {
  const { data } = await apiClient.post<SystemStatusResponse>(
    "/system/warmup"
  );

  return data;
}