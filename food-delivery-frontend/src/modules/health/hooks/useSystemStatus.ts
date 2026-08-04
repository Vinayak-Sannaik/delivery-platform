import { useQuery } from "@tanstack/react-query";

import { getSystemStatus } from "../api/system-status.api";


export function useSystemStatus() {
  return useQuery({
    queryKey: ["system-status"],

    queryFn: getSystemStatus,

    refetchOnWindowFocus: false,

    retry: false,
  });
}