import {
  Button,
  Card,
  Group,
  Stack,
  TextInput,
  Textarea,
  Title,
  Switch,
  Loader,
  Center,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect } from "react";

import {
  createRestaurant,
  updateRestaurant,
} from "../api/restaurants.api";
import { useRestaurant } from "../hooks/useRestaurant";

interface RestaurantFormValues {
  name: string;
  description: string;
  phone: string;
  address: string;
  image_url: string;
  is_active: boolean;
}

export default function RestaurantFormPage() {
  const navigate = useNavigate();
  const { id } = useParams();

  const isEdit = Boolean(id);

  const {
    data: restaurant,
    isLoading,
  } = useRestaurant(id);

  const form = useForm<RestaurantFormValues>({
    initialValues: {
      name: "",
      description: "",
      phone: "",
      address: "",
      image_url: "",
      is_active: true,
    },

    validate: {
      name: (value) =>
        value.trim().length < 2
          ? "Restaurant name is required"
          : null,

      address: (value) =>
        value.trim().length < 3
          ? "Address is required"
          : null,

      phone: (value) =>
        value.trim().length < 5
          ? "Phone number is required"
          : null,
    },
  });

  useEffect(() => {
    if (restaurant) {
      form.setValues({
        name: restaurant.name,
        description: restaurant.description ?? "",
        phone: restaurant.phone ?? "",
        address: restaurant.address ?? "",
        image_url: restaurant.image_url ?? "",
        is_active: restaurant.is_active,
      });
    }
  }, [restaurant]);

  if (isEdit && isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  const handleSubmit = async (
    values: RestaurantFormValues
  ) => {
    try {
      if (isEdit) {
        await updateRestaurant(id!, values);
      } else {
        await createRestaurant(values);
      }

      navigate("/admin/restaurants");
    } catch (error) {
      console.error(
        "Failed to save restaurant:",
        error
      );
    }
  };

  return (
    <Stack>
      <Title order={2}>
        {isEdit
          ? "Edit Restaurant"
          : "Add Restaurant"}
      </Title>

      <Card withBorder maw={700}>
        <form
          onSubmit={form.onSubmit(handleSubmit)}
        >
          <Stack>
            <TextInput
              label="Restaurant Name"
              placeholder="Enter restaurant name"
              withAsterisk
              {...form.getInputProps("name")}
            />

            <Textarea
              label="Description"
              placeholder="Describe the restaurant"
              minRows={3}
              {...form.getInputProps(
                "description"
              )}
            />

            <TextInput
              label="Phone"
              placeholder="Enter phone number"
              withAsterisk
              {...form.getInputProps("phone")}
            />

            <Textarea
              label="Address"
              placeholder="Enter restaurant address"
              minRows={3}
              withAsterisk
              {...form.getInputProps("address")}
            />

            <TextInput
              label="Image URL"
              placeholder="https://..."
              {...form.getInputProps(
                "image_url"
              )}
            />

            {isEdit && (
              <Switch
                label="Active"
                {...form.getInputProps(
                  "is_active",
                  { type: "checkbox" }
                )}
              />
            )}

            <Group justify="flex-end" mt="md">
              <Button
                variant="default"
                onClick={() =>
                  navigate(
                    "/admin/restaurants"
                  )
                }
              >
                Cancel
              </Button>

              <Button type="submit">
                {isEdit
                  ? "Update Restaurant"
                  : "Create Restaurant"}
              </Button>
            </Group>
          </Stack>
        </form>
      </Card>
    </Stack>
  );
}