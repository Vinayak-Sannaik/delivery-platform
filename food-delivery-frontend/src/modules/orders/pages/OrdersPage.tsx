import {
  Badge,
  Card,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from "@mantine/core";

import { useMyOrders } from "../hooks/useMyOrders";

export default function OrdersPage() {
  const { data, isLoading } = useMyOrders();

  if (isLoading) {
    return <Loader />;
  }

  const statusColor: Record<string, string> = {
  PENDING: "yellow",
  CONFIRMED: "blue",
  PREPARING: "cyan",
  READY: "green",
  OUT_FOR_DELIVERY: "violet",
  DELIVERED: "teal",
  CANCELLED: "red",
};

  return (
    <Stack>
      <Title order={2}>My Orders</Title>

      {data?.map((order) => (
        <Card
          key={order.id}
          withBorder
        >
          <Stack>
            <Group justify="space-between">
              <Text fw={600}>
                Order #{order.id.slice(0, 8)}
              </Text>

              <Badge color={statusColor[order.status] ?? "gray"}>
  {order.status}
</Badge>
            </Group>

            <Text>
              ₹{Number(order.total_amount).toFixed(2)}
            </Text>

            {order.items.map((item) => (
              <Text key={item.id}>
                {item.item_name} × {item.quantity}
              </Text>
            ))}
          </Stack>
        </Card>
      ))}
    </Stack>
  );
}