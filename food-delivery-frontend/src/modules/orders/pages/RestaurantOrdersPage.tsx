import {
  Badge,
  Button,
  Card,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useState } from "react";
import { useParams } from "react-router-dom";

import { useRestaurantOrders } from "../hooks/useRestaurantOrders";
import { useUpdateOrderStatus } from "../hooks/useUpdateOrderStatus";

const statusColor: Record<string, string> = {
  PENDING: "yellow",
  CONFIRMED: "blue",
  PREPARING: "cyan",
  READY: "green",
  CANCELLED: "red",
};

export default function RestaurantOrdersPage() {
  const { restaurantId } = useParams();

  const { data, isLoading } = useRestaurantOrders(
    restaurantId!
  );

  const updateStatus = useUpdateOrderStatus();

  const [loadingOrderId, setLoadingOrderId] =
    useState<string | null>(null);

  const handleStatusUpdate = (
    orderId: string,
    status: string,
  ) => {
    setLoadingOrderId(orderId);

    updateStatus.mutate(
      {
        orderId,
        status,
      },
      {
        onSettled: () => {
          setLoadingOrderId(null);
        },
      }
    );
  };

  if (isLoading) {
    return <Loader />;
  }

  return (
    <Stack>
      <Title order={2}>
        Restaurant Orders
      </Title>

      {data?.map((order) => (
        <Card
          key={order.id}
          withBorder
          shadow="sm"
        >
          <Stack>

            <Group justify="space-between">
              <Text fw={700}>
                Order #{order.id.slice(0, 8)}
              </Text>

              <Badge
                color={
                  statusColor[order.status] ??
                  "gray"
                }
              >
                {order.status}
              </Badge>
            </Group>

            <Text fw={600}>
              ₹{Number(order.total_amount).toFixed(2)}
            </Text>

            <Stack gap={4}>
              {order.items.map((item) => (
                <Text key={item.id}>
                  {item.item_name} × {item.quantity}
                </Text>
              ))}
            </Stack>

            <Group mt="md">

              {order.status === "PENDING" && (
                <Button
                  loading={
                    loadingOrderId === order.id
                  }
                  onClick={() =>
                    handleStatusUpdate(
                      order.id,
                      "CONFIRMED"
                    )
                  }
                >
                  Confirm
                </Button>
              )}

              {order.status === "CONFIRMED" && (
                <Button
                  loading={
                    loadingOrderId === order.id
                  }
                  onClick={() =>
                    handleStatusUpdate(
                      order.id,
                      "PREPARING"
                    )
                  }
                >
                  Preparing
                </Button>
              )}

              {order.status === "PREPARING" && (
                <Button
                  color="green"
                  loading={
                    loadingOrderId === order.id
                  }
                  onClick={() =>
                    handleStatusUpdate(
                      order.id,
                      "READY"
                    )
                  }
                >
                  Mark Ready
                </Button>
              )}

            </Group>

          </Stack>
        </Card>
      ))}
    </Stack>
  );
}