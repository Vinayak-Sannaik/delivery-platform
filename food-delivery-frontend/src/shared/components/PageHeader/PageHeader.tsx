import { Stack, Text, Title } from "@mantine/core";

type Props = {
  title: string;
  description?: string;
};

export default function PageHeader({
  title,
  description,
}: Props) {
  return (
    <Stack gap={4}>
      <Title order={2}>
        {title}
      </Title>

      {description && (
        <Text c="dimmed">
          {description}
        </Text>
      )}
    </Stack>
  );
}