import {
  Badge,
  Card,
  Group,
  Text,
} from "@mantine/core";

import type { ServiceStatus } from "../api/system-status.api";


interface Props {
  service: ServiceStatus;
}


export default function ServiceStatusCard({
  service,
}: Props) {
  const healthy = service.status === "healthy";

  return (
    <Card withBorder radius="md" p="md">
      <Group justify="space-between">

        <div>
          <Text fw={600}>
            {service.name}
          </Text>

          {service.latency_ms !== null && (
            <Text size="sm" c="dimmed">
              {service.latency_ms} ms
            </Text>
          )}
        </div>

        <Badge color={healthy ? "green" : "yellow"}>
          {service.status}
        </Badge>

      </Group>
    </Card>
  );
}