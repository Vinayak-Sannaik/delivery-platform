import { apiClient } from "../../../shared/api/client";

export interface Restaurant {
  id: string;
  owner_id: string;
  name: string;
  description: string;
  phone: string;
  address: string;
  image_url: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateRestaurantRequest {
  name: string;
  description: string;
  phone: string;
  address: string;
  image_url: string;
}

export interface UpdateRestaurantRequest {
  name?: string;
  description?: string;
  phone?: string;
  address?: string;
  image_url?: string;
  is_active?: boolean;
}

export async function getRestaurants() {
  const { data } = await apiClient.get<Restaurant[]>(
    "/api/catalog/restaurants"
  );

  return data;
}

export async function getRestaurant(id: string) {
  const { data } = await apiClient.get<Restaurant>(
    `/api/catalog/restaurants/${id}`
  );

  return data;
}

export async function createRestaurant(
  payload: CreateRestaurantRequest
) {
  const { data } = await apiClient.post<Restaurant>(
    "/api/catalog/restaurants",
    payload
  );

  return data;
}

export async function updateRestaurant(
  id: string,
  payload: UpdateRestaurantRequest
) {
  const { data } = await apiClient.put<Restaurant>(
    `/api/catalog/restaurants/${id}`,
    payload
  );

  return data;
}

export async function deleteRestaurant(id: string) {
  await apiClient.delete(`/api/catalog/restaurants/${id}`);
}