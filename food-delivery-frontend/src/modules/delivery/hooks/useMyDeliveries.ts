import { useQuery } from "@tanstack/react-query";

import { getMyDeliveries } from "../api/delivery.api";


export function useMyDeliveries() {
  return useQuery({
    queryKey: ["my-deliveries"],
    queryFn: getMyDeliveries,
    refetchInterval: 5000,
  });
}