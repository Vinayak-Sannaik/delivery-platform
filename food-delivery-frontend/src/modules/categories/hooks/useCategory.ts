import { useQuery } from "@tanstack/react-query";

import { getCategory } from "../api/categories.api";

export function useCategory(id?: string) {
  return useQuery({
    queryKey: ["category", id],
    queryFn: () => getCategory(id!),
    enabled: !!id,
  });
}