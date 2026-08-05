import { useQuery } from "@tanstack/react-query";

import { getCategories } from "../api/categories.api";

export function useCategories(
  restaurantId: string,
) {
  return useQuery({
    queryKey: ["categories", restaurantId],
    queryFn: () => getCategories(restaurantId),
    enabled: !!restaurantId,
  });
}