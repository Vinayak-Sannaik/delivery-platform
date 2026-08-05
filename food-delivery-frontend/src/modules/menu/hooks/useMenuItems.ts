import { useQuery } from "@tanstack/react-query";

import { getMenuItems } from "../api/menu.api";

export function useMenuItems(categoryId?: string) {
  return useQuery({
    queryKey: ["menu-items", categoryId],
    queryFn: () => getMenuItems(categoryId!),
    enabled: !!categoryId,
  });
}