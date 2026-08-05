import { apiClient } from "../../../shared/api/client";

export interface RestaurantOrderItem {
  id: string;
  menu_item_id: string;
  item_name: string;
  quantity: number;
  unit_price: string;
  subtotal: string;
}

export interface RestaurantOrder {
  id: string;
  customer_id: string;
  restaurant_id: string;
  status: string;
  total_amount: string;
  created_at: string;
  updated_at: string;
  items: RestaurantOrderItem[];
}

export async function getRestaurantOrders(
  restaurantId: string,
) {
  const { data } = await apiClient.get<RestaurantOrder[]>(
    `/api/orders/restaurant/${restaurantId}`,
  );

  return data;
}

export async function updateOrderStatus(
  orderId: string,
  status: string,
) {
  const { data } = await apiClient.patch(
    `/api/orders/${orderId}/status`,
    {
      status,
    },
  );

  return data;
}