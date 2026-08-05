import { useQuery } from "@tanstack/react-query";

import { getRestaurants } from "../api/restaurants.api";

export function useRestaurants() {
  return useQuery({
    queryKey: ["restaurants"],
    queryFn: getRestaurants,
  });
}