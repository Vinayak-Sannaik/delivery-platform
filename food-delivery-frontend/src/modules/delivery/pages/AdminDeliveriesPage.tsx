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

import { useAllDeliveries } from "../hooks/useAllDeliveries";
import { useUpdateDeliveryStatus } from "../hooks/useUpdateDeliveryStatus";
import type { Delivery } from "../api/delivery.api";

const statusColor: Record<string, string> = {
  PENDING: "yellow",
  ASSIGNED: "blue",
  PICKED_UP: "cyan",
  DELIVERED: "green",
  CANCELLED: "red",
};

export default function AdminDeliveriesPage() {
  const { data, isLoading } = useAllDeliveries();

  const updateStatus = useUpdateDeliveryStatus();

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
        All Deliveries
      </Title>

      {data?.map((delivery: Delivery) => (
        <Card
          key={delivery.id}
          withBorder
          shadow="sm"
        >
          <Stack>

            <Group justify="space-between">
              <Stack gap={4}>
                <Text fw={600}>
                  Order #
                  {delivery.order_id.slice(0, 8)}
                </Text>

                <Text size="sm">
                  Partner:{" "}
                  {delivery.delivery_partner_id ??
                    "Not Assigned"}
                </Text>
              </Stack>

              <Badge
                color={
                  statusColor[
                    delivery.status
                  ] ?? "gray"
                }
              >
                {delivery.status}
              </Badge>
            </Group>

            <Group mt="md">

              {delivery.status ===
                "PENDING" && (
                <Button
                  loading={
                    loadingOrderId ===
                    delivery.order_id
                  }
                  onClick={() =>
                    handleStatusUpdate(
                      delivery.order_id,
                      "ASSIGNED"
                    )
                  }
                >
                  Assign
                </Button>
              )}

              {delivery.status ===
                "ASSIGNED" && (
                <Button
                  loading={
                    loadingOrderId ===
                    delivery.order_id
                  }
                  onClick={() =>
                    handleStatusUpdate(
                      delivery.order_id,
                      "PICKED_UP"
                    )
                  }
                >
                  Pick Up
                </Button>
              )}

              {delivery.status ===
                "PICKED_UP" && (
                <Button
                  color="green"
                  loading={
                    loadingOrderId ===
                    delivery.order_id
                  }
                  onClick={() =>
                    handleStatusUpdate(
                      delivery.order_id,
                      "DELIVERED"
                    )
                  }
                >
                  Delivered
                </Button>
              )}

            </Group>

          </Stack>
        </Card>
      ))}
    </Stack>
  );
}