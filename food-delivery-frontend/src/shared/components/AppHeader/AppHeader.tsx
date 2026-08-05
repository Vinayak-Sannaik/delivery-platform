import { Burger, Group, Avatar, Text } from "@mantine/core";
import { useUIStore } from "../../store/ui.store";
import { Link } from "react-router-dom";
import { Button } from "@mantine/core";

import { useCartStore} from "../../../modules/cart/store/cart.store";

export default function AppHeader() {
  const { sidebarOpened, toggleSidebar } = useUIStore();

  const items = useCartStore((state) => state.items);

  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
  return (
    <Group justify="space-between" h="100%" px="md">
      <Group>
        <Burger opened={sidebarOpened} onClick={toggleSidebar} />

        <Text fw={700}>Food Delivery Platform</Text>
      </Group>

      <Button component={Link} to="/cart">
        Cart ({totalItems})
      </Button>

      <Avatar radius="xl">V</Avatar>
    </Group>
  );
}
