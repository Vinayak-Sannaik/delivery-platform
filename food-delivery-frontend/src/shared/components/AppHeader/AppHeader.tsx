import {
  Burger,
  Group,
  Avatar,
  Text,
  ActionIcon,
  Indicator,
} from "@mantine/core";
import { IconShoppingCart } from "@tabler/icons-react";
import { Link } from "react-router-dom";

import { useUIStore } from "../../store/ui.store";
import { useCartStore } from "../../../modules/cart/store/cart.store";

export default function AppHeader() {
  const { sidebarOpened, toggleSidebar } = useUIStore();

  const items = useCartStore((state) => state.items);

  const totalItems = items.reduce(
    (sum, item) => sum + item.quantity,
    0
  );

  return (
    <Group
      justify="space-between"
      h="100%"
      px="md"
    >
      <Group>
        <Burger
          opened={sidebarOpened}
          onClick={toggleSidebar}
        />

        <Text fw={700}>
          Food Delivery Platform
        </Text>
      </Group>

      <Group gap="md">
        <Indicator
          inline
          label={totalItems}
          size={16}
          disabled={totalItems === 0}
        >
          <ActionIcon
            component={Link}
            to="/cart"
            variant="subtle"
            size="lg"
          >
            <IconShoppingCart size={24} />
          </ActionIcon>
        </Indicator>

        <Avatar radius="xl">
          V
        </Avatar>
      </Group>
    </Group>
  );
}