import { apiClient } from "../../../shared/api/client";

export interface CreateOrderRequest {
  items: {
    menu_item_id: string;
    quantity: number;
  }[];
}
export interface OrderItem {
  id: string;
  menu_item_id: string;
  item_name: string;
  quantity: number;
  unit_price: string;
  subtotal: string;
}

export interface Order {
  id: string;
  customer_id: string;
  restaurant_id: string;
  status: string;
  total_amount: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export async function createOrder(
  data: CreateOrderRequest,
) {
  const response = await apiClient.post(
    "/api/orders",
    data,
    {
      headers: {
        "Idempotency-Key": crypto.randomUUID(),
      },
    },
  );

  return response.data;
}


export async function getMyOrders() {
  const { data } = await apiClient.get<Order[]>(
    "/api/orders/me",
  );

  return data;
}