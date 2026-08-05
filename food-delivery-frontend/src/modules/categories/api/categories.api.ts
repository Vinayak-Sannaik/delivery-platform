import { apiClient } from "../../../shared/api/client";

export interface Category {
  id: string;
  name: string;
  description: string;
}

export async function getCategories(
  restaurantId: string,
) {
  const { data } = await apiClient.get<Category[]>(
    `/api/catalog/restaurants/${restaurantId}/categories`
  );

  return data;
}