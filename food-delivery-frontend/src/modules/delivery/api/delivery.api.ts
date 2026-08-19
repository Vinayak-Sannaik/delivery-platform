import { apiClient } from "../../../shared/api/client";

export interface Delivery {
  id: string;
  order_id: string;
  delivery_partner_id: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export async function getMyDeliveries() {
  const { data } = await apiClient.get<Delivery[]>(
    "/api/deliveries/me"
  );

  return data;
}

export async function getAllDeliveries() {
  const { data } = await apiClient.get(
    "/api/deliveries"
  );

  return data;
}


export async function updateDeliveryStatus(
  orderId: string,
  status: string,
) {
  const { data } = await apiClient.patch(
    `/api/deliveries/${orderId}/status`,
    {
      status,
    }
  );

  return data;
}