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

export async function getRestaurants() {
  const { data } = await apiClient.get<Restaurant[]>(
    "/api/catalog/restaurants"
  );

  return data;
}

export async function getRestaurant(id: string) {
  const { data } = await apiClient.get(
    `/api/catalog/restaurants/${id}`
  );

  

  return data;
}