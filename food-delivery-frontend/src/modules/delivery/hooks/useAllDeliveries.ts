import { useQuery } from "@tanstack/react-query";
import { getAllDeliveries } from "../api/delivery.api";

export function useAllDeliveries() {
  return useQuery({
    queryKey: ["all-deliveries"],
    queryFn: getAllDeliveries,
  });
}