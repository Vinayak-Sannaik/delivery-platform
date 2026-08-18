import { apiClient } from "../../../shared/api/client";

export interface MenuItem {
  id: string;
  name: string;
  description: string | null;
  price: string;
  is_available: boolean;
}

export interface CreateMenuItemRequest {
  name: string;
  price: number;
  description?: string | null;
  is_available: boolean;
}

export interface UpdateMenuItemRequest {
  name?: string;
  price?: number;
  description?: string | null;
  is_available?: boolean;
}

export async function getMenuItems(categoryId: string) {
  const { data } = await apiClient.get<MenuItem[]>(
    `/api/catalog/${categoryId}/menu_items`
  );

  return data;
}

export async function getMenuItem(id: string) {
  const { data } = await apiClient.get<MenuItem>(
    `/api/catalog/menu-items/${id}`,
  );

  return data;
}

export async function createMenuItem(
  categoryId: string,
  payload: CreateMenuItemRequest,
) {
  const { data } = await apiClient.post<MenuItem>(
    `/api/catalog/${categoryId}/menu_items`,
    payload,
  );

  return data;
}

export async function updateMenuItem(
  id: string,
  payload: UpdateMenuItemRequest,
) {
  const { data } = await apiClient.put<MenuItem>(
    `/api/catalog/menu-items/${id}`,
    payload,
  );

  return data;
}

export async function deleteMenuItem(id: string) {
  await apiClient.delete(
    `/api/catalog/menu-items/${id}`,
  );
}