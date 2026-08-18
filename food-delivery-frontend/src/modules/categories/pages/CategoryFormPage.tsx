import {
  Button,
  Card,
  Center,
  Group,
  Loader,
  Stack,
  TextInput,
  Title,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { useEffect } from "react";

import { useCategory } from "../hooks/useCategory";
import {
  createCategory,
  updateCategory,
} from "../api/categories.api";

interface CategoryFormValues {
  name: string;
}

export default function CategoryFormPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [searchParams] = useSearchParams();

  const restaurantId =
    searchParams.get("restaurantId");

  const isEdit = Boolean(id);

  const {
    data: category,
    isLoading,
  } = useCategory(id);

  const form = useForm<CategoryFormValues>({
    initialValues: {
      name: "",
    },

    validate: {
      name: (value) =>
        value.trim().length < 2
          ? "Category name is required"
          : null,
    },
  });

  useEffect(() => {
    if (category) {
      form.setValues({
        name: category.name,
      });
    }
  }, [category]);

  /*
   * Edit requires the category to be loaded.
   * Create requires restaurantId from the query string.
   */
  if (isEdit && isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  const handleSubmit = async (
    values: CategoryFormValues,
  ) => {
    try {
      if (isEdit) {
        await updateCategory(id!, values);
      } else {
        if (!restaurantId) {
          return;
        }

        await createCategory(
          restaurantId,
          values,
        );
      }

      navigate("/admin/categories");
    } catch (error) {
      console.error(
        "Failed to save category:",
        error,
      );
    }
  };

  return (
    <Stack>
      <Title order={2}>
        {isEdit
          ? "Edit Category"
          : "Add Category"}
      </Title>

      <Card withBorder maw={600}>
        <form
          onSubmit={form.onSubmit(handleSubmit)}
        >
          <Stack>
            <TextInput
              label="Category Name"
              placeholder="e.g. Pizza"
              withAsterisk
              {...form.getInputProps("name")}
            />

            <Group justify="flex-end" mt="md">
              <Button
                variant="default"
                onClick={() =>
                  navigate("/admin/categories")
                }
              >
                Cancel
              </Button>

              <Button type="submit">
                {isEdit
                  ? "Update Category"
                  : "Create Category"}
              </Button>
            </Group>
          </Stack>
        </form>
      </Card>
    </Stack>
  );
}