import {
  Button,
  Card,
  Center,
  Group,
  Loader,
  NumberInput,
  Stack,
  Switch,
  Textarea,
  TextInput,
  Title,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import {
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router-dom";
import { useEffect } from "react";

import { useQuery } from "@tanstack/react-query";

import {
  createMenuItem,
  getMenuItem,
  updateMenuItem,
} from "../../menu/api/menu.api";

interface MenuItemFormValues {
  name: string;
  price: number | string;
  description: string;
  is_available: boolean;
}

export default function MenuItemFormPage() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [searchParams] = useSearchParams();

  const categoryId =
    searchParams.get("categoryId");

  const isEdit = Boolean(id);

  const {
    data: menuItem,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["menu-item", id],
    queryFn: () => getMenuItem(id!),
    enabled: !!id,
  });

  const form = useForm<MenuItemFormValues>({
    initialValues: {
      name: "",
      price: "",
      description: "",
      is_available: true,
    },

    validate: {
      name: (value) =>
        value.trim().length < 1
          ? "Name is required"
          : null,

      price: (value) => {
        const price = Number(value);

        if (Number.isNaN(price)) {
          return "Price is required";
        }

        if (price <= 0) {
          return "Price must be greater than 0";
        }

        return null;
      },
    },
  });

  useEffect(() => {
    if (menuItem) {
      form.setValues({
        name: menuItem.name,
        price: Number(menuItem.price),
        description:
          menuItem.description ?? "",
        is_available: menuItem.is_available,
      });
    }
  }, [menuItem]);

  if (isEdit && isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (isEdit && isError) {
    return (
      <Center py="xl">
        Failed to load menu item.
      </Center>
    );
  }

  const handleSubmit = async (
    values: MenuItemFormValues,
  ) => {
    if (!isEdit && !categoryId) {
      console.error(
        "Category ID is required",
      );
      return;
    }

    try {
      const payload = {
        name: values.name.trim(),
        price: Number(values.price),
        description:
          values.description.trim() || null,
        is_available: values.is_available,
      };

      if (isEdit) {
        await updateMenuItem(id!, payload);
      } else {
        await createMenuItem(
          categoryId!,
          payload,
        );
      }

      navigate("/admin/menu-items");
    } catch (error) {
      console.error(
        "Failed to save menu item:",
        error,
      );
    }
  };

  return (
    <Stack>
      <Title order={2}>
        {isEdit
          ? "Edit Menu Item"
          : "Add Menu Item"}
      </Title>

      <Card
        withBorder
        maw={600}
      >
        <form
          onSubmit={form.onSubmit(handleSubmit)}
        >
          <Stack>
            <TextInput
              label="Name"
              placeholder="e.g. Margherita Pizza"
              withAsterisk
              {...form.getInputProps("name")}
            />

            <NumberInput
              label="Price"
              placeholder="e.g. 299"
              prefix="₹"
              min={0}
              decimalScale={2}
              fixedDecimalScale={false}
              withAsterisk
              {...form.getInputProps("price")}
            />

            <Textarea
              label="Description"
              placeholder="Describe the menu item"
              minRows={4}
              autosize
              {...form.getInputProps(
                "description",
              )}
            />

            <Switch
              label="Available"
              {...form.getInputProps(
                "is_available",
                {
                  type: "checkbox",
                },
              )}
            />

            <Group
              justify="flex-end"
              mt="md"
            >
              <Button
                variant="default"
                onClick={() =>
                  navigate(
                    "/admin/menu-items",
                  )
                }
              >
                Cancel
              </Button>

              <Button type="submit">
                {isEdit
                  ? "Update Menu Item"
                  : "Create Menu Item"}
              </Button>
            </Group>
          </Stack>
        </form>
      </Card>
    </Stack>
  );
}