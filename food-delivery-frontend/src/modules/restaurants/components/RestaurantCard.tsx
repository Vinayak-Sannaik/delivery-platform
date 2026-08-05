import {
  Badge,
  Button,
  Card,
  Group,
  Image,
  Stack,
  Text,
} from "@mantine/core";

import { useNavigate } from "react-router-dom";

import type { Restaurant } from "../api/restaurants.api";

interface RestaurantCardProps {
  restaurant: Restaurant;
}

export default function RestaurantCard({
  restaurant,
}: RestaurantCardProps) {
  const navigate = useNavigate();

  return (
    <Card shadow="sm" withBorder radius="md">
      <Card.Section>
        <Image
          src={
            restaurant.image_url ||
            "https://placehold.co/600x300?text=Restaurant"
          }
          h={180}
          alt={restaurant.name}
        />
      </Card.Section>

      <Stack mt="md" gap="xs">
        <Group justify="space-between">
          <Text fw={700}>
            {restaurant.name}
          </Text>

          <Badge
            color={
              restaurant.is_active
                ? "green"
                : "red"
            }
          >
            {restaurant.is_active
              ? "Open"
              : "Closed"}
          </Badge>
        </Group>

        <Text c="dimmed" lineClamp={2}>
          {restaurant.description}
        </Text>

        <Text size="sm">
          {restaurant.address}
        </Text>

        <Button
          fullWidth
          mt="sm"
          onClick={() =>
            navigate(`/restaurants/${restaurant.id}`)
          }
        >
          View Menu
        </Button>
      </Stack>
    </Card>
  );
}