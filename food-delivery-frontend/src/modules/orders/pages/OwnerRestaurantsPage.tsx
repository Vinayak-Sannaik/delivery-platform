import {
  Button,
  Card,
  Group,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useNavigate } from "react-router-dom";

import { useRestaurants } from "../../restaurants/hooks/useRestaurants";
import { useAuthStore } from "../../auth/store/auth.store";

export default function OwnerRestaurantsPage() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);

  const { data } = useRestaurants();

  const restaurants =
    data?.filter(
      (restaurant) =>
        restaurant.owner_id === user?.id,
    ) ?? [];

  return (
    <Stack>
      <Title order={2}>
        My Restaurants
      </Title>

      {restaurants.map((restaurant) => (
        <Card
          key={restaurant.id}
          withBorder
        >
          <Group justify="space-between">
            <Stack gap={2}>
              <Text fw={700}>
                {restaurant.name}
              </Text>

              <Text c="dimmed">
                {restaurant.address}
              </Text>
            </Stack>

            <Button
              onClick={() =>
                navigate(
                  `/owner/restaurants/${restaurant.id}/orders`,
                )
              }
            >
              View Orders
            </Button>
          </Group>
        </Card>
      ))}
    </Stack>
  );
}