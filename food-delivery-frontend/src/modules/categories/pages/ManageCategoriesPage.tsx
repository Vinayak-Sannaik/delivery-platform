import {
  ActionIcon,
  Button,
  Card,
  Center,
  Group,
  Loader,
  Select,
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
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useRestaurants } from "../../restaurants/hooks/useRestaurants";
import { useCategories } from "../hooks/useCategories";
import { deleteCategory } from "../api/categories.api";

export default function ManageCategoriesPage() {
  const navigate = useNavigate();

  const [restaurantId, setRestaurantId] =
    useState<string | null>(null);

  const {
    data: restaurants,
    isLoading: restaurantsLoading,
  } = useRestaurants();

  const {
    data: categories,
    isLoading: categoriesLoading,
    isError,
    refetch,
  } = useCategories(restaurantId ?? "");

  const handleDelete = async (id: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this category?",
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteCategory(id);
      await refetch();
    } catch (error) {
      console.error(
        "Failed to delete category:",
        error,
      );
    }
  };

  const restaurantOptions =
    restaurants?.map((restaurant) => ({
      value: restaurant.id,
      label: restaurant.name,
    })) ?? [];

  return (
    <Stack>
      <Group justify="space-between">
        <Title order={2}>
          Manage Categories
        </Title>

        <Button
          leftSection={<IconPlus size={18} />}
          disabled={!restaurantId}
          onClick={() =>
            navigate(
              `/admin/categories/new?restaurantId=${restaurantId}`,
            )
          }
        >
          Add Category
        </Button>
      </Group>

      <Card withBorder>
        <Select
          label="Restaurant"
          placeholder="Select a restaurant"
          searchable
          clearable
          data={restaurantOptions}
          value={restaurantId}
          onChange={setRestaurantId}
          disabled={restaurantsLoading}
        />
      </Card>

      {!restaurantId && (
        <Card withBorder>
          <Center py="xl">
            <Text c="dimmed">
              Select a restaurant to view its categories.
            </Text>
          </Center>
        </Card>
      )}

      {restaurantId && categoriesLoading && (
        <Center py="xl">
          <Loader />
        </Center>
      )}

      {restaurantId && isError && (
        <Stack>
          <Text c="red">
            Failed to load categories.
          </Text>

          <Button onClick={() => refetch()}>
            Retry
          </Button>
        </Stack>
      )}

      {restaurantId &&
        !categoriesLoading &&
        !isError && (
          <Card withBorder>
            {categories?.length === 0 ? (
              <Center py="xl">
                <Stack align="center">
                  <Text c="dimmed">
                    No categories found.
                  </Text>

                  <Button
                    leftSection={
                      <IconPlus size={18} />
                    }
                    onClick={() =>
                      navigate(
                        `/admin/categories/new?restaurantId=${restaurantId}`,
                      )
                    }
                  >
                    Create Category
                  </Button>
                </Stack>
              </Center>
            ) : (
              <Table>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>
                      Category
                    </Table.Th>

                    <Table.Th>
                      Actions
                    </Table.Th>
                  </Table.Tr>
                </Table.Thead>

                <Table.Tbody>
                  {categories?.map((category) => (
                    <Table.Tr key={category.id}>
                      <Table.Td>
                        <Text fw={600}>
                          {category.name}
                        </Text>
                      </Table.Td>

                      <Table.Td>
                        <Group gap="xs">
                          <Tooltip label="Edit category">
                            <ActionIcon
                              variant="light"
                              onClick={() =>
                                navigate(
                                  `/admin/categories/${category.id}/edit`,
                                )
                              }
                            >
                              <IconEdit
                                size={18}
                              />
                            </ActionIcon>
                          </Tooltip>

                          <Tooltip label="Delete category">
                            <ActionIcon
                              color="red"
                              variant="light"
                              onClick={() =>
                                handleDelete(
                                  category.id,
                                )
                              }
                            >
                              <IconTrash
                                size={18}
                              />
                            </ActionIcon>
                          </Tooltip>
                        </Group>
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            )}
          </Card>
        )}
    </Stack>
  );
}