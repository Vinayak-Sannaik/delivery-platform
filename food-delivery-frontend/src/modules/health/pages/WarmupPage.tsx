import { Center, Loader, Stack, Text } from "@mantine/core";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useHealth } from "../hooks/useHealth";

export default function WarmupPage() {
  const { data, isPending, isError } = useHealth();
  const navigate = useNavigate();

  useEffect(() => {
    if (data?.status === "healthy") {
      const timer = setTimeout(() => {
        navigate("/login", { replace: true });
      }, 1500);

      return () => clearTimeout(timer);
    }
  }, [data, navigate]);

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
        <Text c="red">Failed to connect to the backend.</Text>
      </Center>
    );
  }

  return (
    <Center mih="100vh">
      <Stack align="center">
        <Text fw={700} size="xl">
          Backend Ready 🚀
        </Text>

        <Text c="dimmed">Redirecting to login...</Text>
      </Stack>
    </Center>
  );
}
