import { apiClient } from "../../../shared/api/client";

export interface Category {
  id: string;
  name: string;
  restaurant_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateCategoryRequest {
  name: string;
}

export interface UpdateCategoryRequest {
  name?: string;
}

export async function getCategories(
  restaurantId: string,
) {
  const { data } = await apiClient.get<Category[]>(
    `/api/catalog/restaurants/${restaurantId}/categories`,
  );

  return data;
}

export async function getCategory(id: string) {
  const { data } = await apiClient.get<Category>(
    `/api/catalog/categories/${id}`,
  );

  return data;
}

export async function createCategory(
  restaurantId: string,
  payload: CreateCategoryRequest,
) {
  const { data } = await apiClient.post<Category>(
    `/api/catalog/restaurants/${restaurantId}/categories`,
    payload,
  );

  return data;
}

export async function updateCategory(
  id: string,
  payload: UpdateCategoryRequest,
) {
  const { data } = await apiClient.put<Category>(
    `/api/catalog/categories/${id}`,
    payload,
  );

  return data;
}

export async function deleteCategory(
  id: string,
): Promise<void> {
  await apiClient.delete(
    `/api/catalog/categories/${id}`,
  );
}