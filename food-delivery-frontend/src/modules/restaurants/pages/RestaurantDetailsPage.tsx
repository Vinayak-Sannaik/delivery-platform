import { useParams } from "react-router-dom";
import {
  Loader,
  Center,
  Title,
  Text,
  Button,
  Card,
  Group,
} from "@mantine/core";

import { useRestaurant } from "../hooks/useRestaurant";
import { useCategories } from "../../categories/hooks/useCategories";
import { useMenuItems } from "../../menu/hooks/useMenuItems";

import { useState } from "react";

import { useCartStore } from "../../cart/store/cart.store";

export default function RestaurantDetailsPage() {
  const { id } = useParams();

  const { data, isLoading } = useRestaurant(id!);
  const { data: categories } = useCategories(id!);

  const [selectedCategory, setSelectedCategory] = useState<string>();

  const { data: menuItems } = useMenuItems(selectedCategory);

  const addItem = useCartStore((state) => state.addItem);

  if (isLoading) {
    return (
      <Center>
        <Loader />
      </Center>
    );
  }

  if (!data) {
    return <Text>Restaurant not found.</Text>;
  }

  return (
    <>
      <Title>{data.name}</Title>

      <Text mt="md">{data.description}</Text>

      <Text mt="md">{data.address}</Text>

      <Title order={3} mt="xl">
        Categories
      </Title>

      {categories?.map((category) => (
        <Button
          key={category.id}
          onClick={() => setSelectedCategory(category.id)}
        >
          {category.name}
        </Button>
      ))}

      {menuItems?.map((item) => (
        <Card key={item.id} mt="md" withBorder>
          <Group justify="space-between">
            <div>
              <Text fw={600}>{item.name}</Text>

              <Text size="sm">{item.description}</Text>
            </div>

            <Text fw={700}>₹{item.price}</Text>

            <Button
              onClick={() =>
                addItem({
                  menuItemId: item.id,
                  restaurantId: id!,
                  name: item.name,
                  price: Number(item.price),
                })
              }
            >
              Add to Cart
            </Button>
          </Group>
        </Card>
      ))}
    </>
  );
}
