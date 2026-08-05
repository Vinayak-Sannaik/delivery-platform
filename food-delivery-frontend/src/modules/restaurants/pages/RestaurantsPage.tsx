import {
  Alert,
  Center,
  Loader,
  SimpleGrid,
  Text,
  Title,
} from "@mantine/core";

import RestaurantCard from "../components/RestaurantCard";
import { useRestaurants } from "../hooks/useRestaurants";

export default function RestaurantsPage() {
  const {
    data: restaurants,
    isLoading,
    isError,
  } = useRestaurants();

  if (isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (isError) {
    return (
      <Alert color="red">
        Failed to load restaurants.
      </Alert>
    );
  }

  return (
    <>
      <Title mb="md">
        Restaurants
      </Title>

      {restaurants?.length === 0 ? (
        <Text>No restaurants found.</Text>
      ) : (
        <SimpleGrid cols={3}>
          {restaurants?.map((restaurant) => (
            <RestaurantCard
              key={restaurant.id}
              restaurant={restaurant}
            />
          ))}
        </SimpleGrid>
      )}
    </>
  );
}