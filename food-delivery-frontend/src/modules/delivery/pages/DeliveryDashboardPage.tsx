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

import { useMyDeliveries } from "../hooks/useMyDeliveries";
import { useUpdateDeliveryStatus } from "../hooks/useUpdateDeliveryStatus";


const statusColor: Record<string, string> = {
  PENDING: "yellow",
  ASSIGNED: "blue",
  PICKED_UP: "cyan",
  DELIVERED: "green",
  CANCELLED: "red",
};


export default function DeliveryDashboardPage() {

  const {
    data,
    isLoading,
  } = useMyDeliveries();


  const updateStatus =
    useUpdateDeliveryStatus();


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
        My Deliveries
      </Title>


      {data?.length === 0 && (
        <Text c="dimmed">
          No deliveries assigned yet.
        </Text>
      )}


      {data?.map((delivery) => (

        <Card
          key={delivery.id}
          withBorder
          shadow="sm"
        >

          <Stack>

            <Group justify="space-between">

              <Text fw={700}>
                Order #
                {delivery.order_id.slice(0, 8)}
              </Text>


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



            <Group>

              {delivery.status === "ASSIGNED" && (

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



              {delivery.status === "PICKED_UP" && (

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
                  Mark Delivered
                </Button>

              )}


            </Group>

          </Stack>

        </Card>

      ))}


    </Stack>
  );
}