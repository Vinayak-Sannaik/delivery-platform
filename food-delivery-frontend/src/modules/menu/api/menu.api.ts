import { apiClient } from "../../../shared/api/client";

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: string;
  is_available: boolean;
}

export async function getMenuItems(categoryId: string) {
  const { data } = await apiClient.get<MenuItem[]>(
    `/api/catalog/${categoryId}/menu_items`
  );

  return data;
}