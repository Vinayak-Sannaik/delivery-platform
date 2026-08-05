import { useQuery } from "@tanstack/react-query";

import { getMyOrders } from "../api/orders.api";

export function useMyOrders() {
  return useQuery({
    queryKey: ["my-orders"],
    queryFn: getMyOrders,

    refetchInterval: 5000,
  });
}
