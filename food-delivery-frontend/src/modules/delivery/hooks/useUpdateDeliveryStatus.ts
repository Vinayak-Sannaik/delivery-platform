import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import { updateDeliveryStatus } from "../api/delivery.api";

export function useUpdateDeliveryStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      orderId,
      status,
    }: {
      orderId: string;
      status: string;
    }) =>
      updateDeliveryStatus(
        orderId,
        status,
      ),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["my-deliveries"],
      });

      queryClient.invalidateQueries({
        queryKey: ["all-deliveries"],
      });
    },
  });
}