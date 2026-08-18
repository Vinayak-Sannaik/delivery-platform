import {
  ActionIcon,
  Badge,
  Button,
  Card,
  Center,
  Group,
  Loader,
  Stack,
  Table,
  Text,
  Title,
  Tooltip,
} from "@mantine/core";
import {
  IconEdit,
  IconPlus,
  IconTrash,
} from "@tabler/icons-react";
import { useNavigate } from "react-router-dom";

import { useRestaurants } from "../hooks/useRestaurants";
import { deleteRestaurant } from "../api/restaurants.api";

export default function ManageRestaurantsPage() {
  const navigate = useNavigate();

  const {
    data: restaurants,
    isLoading,
    isError,
    refetch,
  } = useRestaurants();

  const handleDelete = async (id: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this restaurant?"
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteRestaurant(id);
      await refetch();
    } catch (error) {
      console.error("Failed to delete restaurant:", error);
    }
  };

  if (isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (isError) {
    return (
      <Stack>
        <Title order={2}>Manage Restaurants</Title>

        <Text c="red">
          Failed to load restaurants.
        </Text>

        <Button onClick={() => refetch()}>
          Retry
        </Button>
      </Stack>
    );
  }

  return (
    <Stack>
      <Group justify="space-between">
        <Title order={2}>Manage Restaurants</Title>

        <Button
          leftSection={<IconPlus size={18} />}
          onClick={() => navigate("/admin/restaurants/new")}
        >
          Add Restaurant
        </Button>
      </Group>

      <Card withBorder>
        {restaurants?.length === 0 ? (
          <Stack align="center" py="xl">
            <Text c="dimmed">
              No restaurants found.
            </Text>

            <Button
              leftSection={<IconPlus size={18} />}
              onClick={() =>
                navigate("/admin/restaurants/new")
              }
            >
              Create Restaurant
            </Button>
          </Stack>
        ) : (
          <Table.ScrollContainer minWidth={900}>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Name</Table.Th>
                  <Table.Th>Phone</Table.Th>
                  <Table.Th>Address</Table.Th>
                  <Table.Th>Status</Table.Th>
                  <Table.Th>Actions</Table.Th>
                </Table.Tr>
              </Table.Thead>

              <Table.Tbody>
                {restaurants?.map((restaurant) => (
                  <Table.Tr key={restaurant.id}>
                    <Table.Td>
                      <Text fw={600}>
                        {restaurant.name}
                      </Text>
                    </Table.Td>

                    <Table.Td>
                      {restaurant.phone || "-"}
                    </Table.Td>

                    <Table.Td>
                      <Text lineClamp={1}>
                        {restaurant.address || "-"}
                      </Text>
                    </Table.Td>

                    <Table.Td>
                      <Badge
                        color={
                          restaurant.is_active
                            ? "green"
                            : "gray"
                        }
                      >
                        {restaurant.is_active
                          ? "Active"
                          : "Inactive"}
                      </Badge>
                    </Table.Td>

                    <Table.Td>
                      <Group gap="xs">
                        <Tooltip label="Edit restaurant">
                          <ActionIcon
                            variant="light"
                            onClick={() =>
                              navigate(
                                `/admin/restaurants/${restaurant.id}/edit`
                              )
                            }
                          >
                            <IconEdit size={18} />
                          </ActionIcon>
                        </Tooltip>

                        <Tooltip label="Delete restaurant">
                          <ActionIcon
                            color="red"
                            variant="light"
                            onClick={() =>
                              handleDelete(
                                restaurant.id
                              )
                            }
                          >
                            <IconTrash size={18} />
                          </ActionIcon>
                        </Tooltip>
                      </Group>
                    </Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </Table.ScrollContainer>
        )}
      </Card>
    </Stack>
  );
}