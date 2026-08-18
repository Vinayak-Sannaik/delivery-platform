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
import { useCategories } from "../../categories/hooks/useCategories";
import { useMenuItems } from "../../menu/hooks/useMenuItems";
import { deleteMenuItem } from "../../menu/api/menu.api";

export default function ManageMenuItemsPage() {
  const navigate = useNavigate();

  const [restaurantId, setRestaurantId] =
    useState<string | null>(null);

  const [categoryId, setCategoryId] =
    useState<string | null>(null);

  const {
    data: restaurants,
    isLoading: restaurantsLoading,
  } = useRestaurants();

  const {
    data: categories,
    isLoading: categoriesLoading,
  } = useCategories(restaurantId ?? "");

  const {
    data: menuItems,
    isLoading: menuItemsLoading,
    isError,
    refetch,
  } = useMenuItems(categoryId ?? undefined);

  const handleRestaurantChange = (
    value: string | null,
  ) => {
    setRestaurantId(value);

    // Category belongs to the previous restaurant.
    // Clear it immediately.
    setCategoryId(null);
  };

  const handleDelete = async (id: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this menu item?",
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteMenuItem(id);
      await refetch();
    } catch (error) {
      console.error(
        "Failed to delete menu item:",
        error,
      );
    }
  };

  const restaurantOptions =
    restaurants?.map((restaurant) => ({
      value: restaurant.id,
      label: restaurant.name,
    })) ?? [];

  const categoryOptions =
    categories?.map((category) => ({
      value: category.id,
      label: category.name,
    })) ?? [];

  return (
    <Stack>
      <Group justify="space-between">
        <Title order={2}>
          Manage Menu Items
        </Title>

        <Button
          leftSection={<IconPlus size={18} />}
          disabled={!categoryId}
          onClick={() =>
            navigate(
              `/admin/menu-items/new?categoryId=${categoryId}`,
            )
          }
        >
          Add Menu Item
        </Button>
      </Group>

      <Card withBorder>
        <Stack>
          <Select
            label="Restaurant"
            placeholder="Select restaurant"
            searchable
            clearable
            data={restaurantOptions}
            value={restaurantId}
            onChange={handleRestaurantChange}
            disabled={restaurantsLoading}
          />

          <Select
            label="Category"
            placeholder={
              restaurantId
                ? "Select category"
                : "Select restaurant first"
            }
            searchable
            clearable
            data={categoryOptions}
            value={categoryId}
            onChange={setCategoryId}
            disabled={
              !restaurantId ||
              categoriesLoading
            }
          />
        </Stack>
      </Card>

      {!categoryId && (
        <Card withBorder>
          <Center py="xl">
            <Text c="dimmed">
              Select a restaurant and category to
              view menu items.
            </Text>
          </Center>
        </Card>
      )}

      {categoryId && menuItemsLoading && (
        <Center py="xl">
          <Loader />
        </Center>
      )}

      {categoryId && isError && (
        <Stack>
          <Text c="red">
            Failed to load menu items.
          </Text>

          <Button onClick={() => refetch()}>
            Retry
          </Button>
        </Stack>
      )}

      {categoryId &&
        !menuItemsLoading &&
        !isError && (
          <Card withBorder>
            {menuItems?.length === 0 ? (
              <Center py="xl">
                <Stack align="center">
                  <Text c="dimmed">
                    No menu items found.
                  </Text>

                  <Button
                    leftSection={
                      <IconPlus size={18} />
                    }
                    onClick={() =>
                      navigate(
                        `/admin/menu-items/new?categoryId=${categoryId}`,
                      )
                    }
                  >
                    Create Menu Item
                  </Button>
                </Stack>
              </Center>
            ) : (
              <Table>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>
                      Name
                    </Table.Th>

                    <Table.Th>
                      Description
                    </Table.Th>

                    <Table.Th>
                      Price
                    </Table.Th>

                    <Table.Th>
                      Available
                    </Table.Th>

                    <Table.Th>
                      Actions
                    </Table.Th>
                  </Table.Tr>
                </Table.Thead>

                <Table.Tbody>
                  {menuItems?.map((item) => (
                    <Table.Tr key={item.id}>
                      <Table.Td>
                        <Text fw={600}>
                          {item.name}
                        </Text>
                      </Table.Td>

                      <Table.Td>
                        <Text
                          size="sm"
                          c="dimmed"
                        >
                          {item.description ||
                            "—"}
                        </Text>
                      </Table.Td>

                      <Table.Td>
                        ₹{item.price}
                      </Table.Td>

                      <Table.Td>
                        {item.is_available
                          ? "Yes"
                          : "No"}
                      </Table.Td>

                      <Table.Td>
                        <Group gap="xs">
                          <Tooltip label="Edit menu item">
                            <ActionIcon
                              variant="light"
                              onClick={() =>
                                navigate(
                                  `/admin/menu-items/${item.id}/edit?categoryId=${categoryId}`,
                                )
                              }
                            >
                              <IconEdit
                                size={18}
                              />
                            </ActionIcon>
                          </Tooltip>

                          <Tooltip label="Delete menu item">
                            <ActionIcon
                              color="red"
                              variant="light"
                              onClick={() =>
                                handleDelete(
                                  item.id,
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