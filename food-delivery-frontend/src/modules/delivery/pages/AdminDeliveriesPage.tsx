import {
  Badge,
  Card,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from "@mantine/core";

import { useAllDeliveries } from "../hooks/useAllDeliveries";


const statusColor: Record<string, string> = {
  PENDING: "yellow",
  ASSIGNED: "blue",
  PICKED_UP: "cyan",
  DELIVERED: "green",
  CANCELLED: "red",
};


export default function AdminDeliveriesPage() {

  const {
    data,
    isLoading,
  } = useAllDeliveries();


  if (isLoading) {
    return <Loader />;
  }


  return (
    <Stack>

      <Title order={2}>
        All Deliveries
      </Title>


      {data?.map((delivery) => (

        <Card
          key={delivery.id}
          withBorder
        >

          <Group justify="space-between">

            <Stack gap={4}>
              <Text fw={600}>
                Order #
                {delivery.order_id.slice(0, 8)}
              </Text>

              <Text size="sm">
                Partner:
                {" "}
                {delivery.delivery_partner_id}
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

        </Card>

      ))}

    </Stack>
  );
}