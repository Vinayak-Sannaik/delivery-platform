import { Group, ThemeIcon, Text } from "@mantine/core";
import { IconChefHat } from "@tabler/icons-react";

export default function AppLogo() {
  return (
    <Group gap="xs">
      <ThemeIcon
        size={42}
        radius="md"
        variant="filled"
      >
        <IconChefHat size={24} />
      </ThemeIcon>

      <div>
        <Text fw={700}>
          Food Delivery
        </Text>

        <Text
          size="xs"
          c="dimmed"
        >
          Microservices Platform
        </Text>
      </div>
    </Group>
  );
}