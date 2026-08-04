import { Center, Loader, Stack, Text } from "@mantine/core";

import { useHealth } from "../hooks/useHealth";

export default function WarmupPage() {
  const { data, isPending, isError } = useHealth();

  if (isPending) {
    return (
      <Center mih="100vh">
        <Stack align="center">
          <Loader size="lg" />
          <Text>Waking up backend services...</Text>
        </Stack>
      </Center>
    );
  }

  if (isError) {
    return (
      <Center mih="100vh">
        <Text c="red">
          Failed to connect to the backend.
        </Text>
      </Center>
    );
  }

  return (
    <Center mih="100vh">
      <Stack align="center">
        <Text fw={700}>Backend is ready 🚀</Text>
        <Text>Status: {data.status}</Text>
      </Stack>
    </Center>
  );
}