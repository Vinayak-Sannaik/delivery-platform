import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import { updateOrderStatus } from "../api/restaurant-orders.api";

export function useUpdateOrderStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      orderId,
      status,
    }: {
      orderId: string;
      status: string;
    }) =>
      updateOrderStatus(orderId, status),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["restaurant-orders"],
      });
    },
  });
}