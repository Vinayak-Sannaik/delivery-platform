import { Burger, Group, Avatar, Text } from "@mantine/core";
import { useUIStore } from "../../store/ui.store";

export default function AppHeader() {
  const { sidebarOpened, toggleSidebar } = useUIStore();

  return (
    <Group justify="space-between" h="100%" px="md">
      <Group>
        <Burger
          opened={sidebarOpened}
          onClick={toggleSidebar}
        />

        <Text fw={700}>
          Food Delivery Platform
        </Text>
      </Group>

      <Avatar radius="xl">
        V
      </Avatar>
    </Group>
  );
}