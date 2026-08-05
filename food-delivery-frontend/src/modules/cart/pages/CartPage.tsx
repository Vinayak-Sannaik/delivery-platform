import {
  ActionIcon,
  Button,
  Card,
  Center,
  Group,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { IconMinus, IconPlus, IconTrash } from "@tabler/icons-react";
import { useNavigate } from "react-router-dom";

import { useCartStore } from "../store/cart.store";
import { useCreateOrder } from "../../orders/hooks/useCreateOrder";

export default function CartPage() {
  const navigate = useNavigate();

  const mutation = useCreateOrder();

  const items = useCartStore((state) => state.items);

  const increase = useCartStore((state) => state.increase);
  const decrease = useCartStore((state) => state.decrease);
  const removeItem = useCartStore((state) => state.removeItem);
  const clear = useCartStore((state) => state.clear);

  const totalItems = items.reduce(
    (sum, item) => sum + item.quantity,
    0,
  );

  const totalPrice = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  const handleCheckout = async () => {
    try {
      await mutation.mutateAsync({
        items: items.map((item) => ({
          menu_item_id: item.menuItemId,
          quantity: item.quantity,
        })),
      });

      clear();

      notifications.show({
        title: "Success",
        message: "Order placed successfully.",
        color: "green",
      });

      navigate("/orders");
    } catch (error) {
      console.error(error);

      notifications.show({
        title: "Checkout Failed",
        message: "Unable to place your order.",
        color: "red",
      });
    }
  };

  if (items.length === 0) {
    return (
      <Center h="70vh">
        <Stack align="center">
          <Title order={2}>Your cart is empty</Title>

          <Text c="dimmed">
            Add some delicious food to get started.
          </Text>
        </Stack>
      </Center>
    );
  }

  return (
    <Stack>
      <Group justify="space-between">
        <Title order={2}>My Cart</Title>

        <Button
          color="red"
          variant="light"
          onClick={clear}
        >
          Clear Cart
        </Button>
      </Group>

      {items.map((item) => (
        <Card
          key={item.menuItemId}
          withBorder
          shadow="sm"
        >
          <Group justify="space-between" align="center">
            <Stack gap={4}>
              <Text fw={600}>
                {item.name}
              </Text>

              <Text c="dimmed">
                ₹{item.price}
              </Text>
            </Stack>

            <Group>
              <ActionIcon
                variant="light"
                onClick={() => decrease(item.menuItemId)}
              >
                <IconMinus size={16} />
              </ActionIcon>

              <Text fw={600}>
                {item.quantity}
              </Text>

              <ActionIcon
                variant="light"
                onClick={() => increase(item.menuItemId)}
              >
                <IconPlus size={16} />
              </ActionIcon>

              <ActionIcon
                color="red"
                variant="light"
                onClick={() => removeItem(item.menuItemId)}
              >
                <IconTrash size={16} />
              </ActionIcon>
            </Group>
          </Group>
        </Card>
      ))}

      <Card withBorder>
        <Stack>
          <Group justify="space-between">
            <Text>Total Items</Text>

            <Text fw={700}>
              {totalItems}
            </Text>
          </Group>

          <Group justify="space-between">
            <Text>Total Price</Text>

            <Title order={3}>
              ₹{totalPrice.toFixed(2)}
            </Title>
          </Group>

          <Button
            size="md"
            fullWidth
            loading={mutation.isPending}
            onClick={handleCheckout}
          >
            Checkout
          </Button>
        </Stack>
      </Card>
    </Stack>
  );
}