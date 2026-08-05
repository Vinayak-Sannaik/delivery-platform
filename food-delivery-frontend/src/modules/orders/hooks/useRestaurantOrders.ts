import { useQuery } from "@tanstack/react-query";

import { getRestaurantOrders } from "../api/restaurant-orders.api";

export function useRestaurantOrders(
  restaurantId: string,
) {
  return useQuery({
    queryKey: ["restaurant-orders", restaurantId],
    queryFn: () => getRestaurantOrders(restaurantId),
    enabled: !!restaurantId,
    refetchInterval: 5000,
  });
}