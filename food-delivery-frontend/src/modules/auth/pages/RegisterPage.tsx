import {
  Button,
  Paper,
  PasswordInput,
  Select,
  Stack,
  TextInput,
  Title,
  Text,
  Anchor,
} from "@mantine/core";

import { useForm } from "@mantine/form";
import { Link, useNavigate } from "react-router-dom";

import { useRegister } from "../hooks/useRegister";

type RegisterFormValues = {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  password: string;
  confirm_password: string;
  role: "CUSTOMER" | "RESTAURANT_OWNER";
};

export default function RegisterPage() {
  const navigate = useNavigate();
  const registerMutation = useRegister();

  const form = useForm<RegisterFormValues>({
    initialValues: {
      first_name: "",
      last_name: "",
      email: "",
      phone: "",
      password: "",
      confirm_password: "",
      role: "CUSTOMER",
    },

    validate: {
      first_name: (value) =>
        value.trim().length < 1
          ? "First name is required"
          : null,

      last_name: (value) =>
        value.trim().length < 1
          ? "Last name is required"
          : null,

      email: (value) =>
        /^\S+@\S+\.\S+$/.test(value)
          ? null
          : "Invalid email",

      phone: (value) =>
        /^\d{10,20}$/.test(value)
          ? null
          : "Phone must contain 10-20 digits",

      password: (value) =>
        value.length < 8
          ? "Password must be at least 8 characters"
          : null,

      confirm_password: (value, values) =>
        value !== values.password
          ? "Passwords do not match"
          : null,

      role: (value) =>
        !value
          ? "Please select an account type"
          : null,
    },
  });

  const handleSubmit = form.onSubmit(
    async (values) => {
      try {
        await registerMutation.mutateAsync({
          first_name: values.first_name,
          last_name: values.last_name,
          email: values.email,
          phone: values.phone,
          password: values.password,
          role: values.role,
        });

        navigate("/login", {
          replace: true,
          state: {
            message:
              "Account created successfully. Please login.",
          },
        });
      } catch (error) {
        console.error(
          "Registration failed:",
          error,
        );
      }
    },
  );

  return (
    <Paper
      maw={500}
      mx="auto"
      p="xl"
      withBorder
    >
      <form onSubmit={handleSubmit}>
        <Stack>
          <Title order={2}>
            Create Account
          </Title>

          <Text c="dimmed" size="sm">
            Create your Food Delivery Platform account.
          </Text>

          <TextInput
            label="First Name"
            placeholder="John"
            withAsterisk
            {...form.getInputProps("first_name")}
          />

          <TextInput
            label="Last Name"
            placeholder="Doe"
            withAsterisk
            {...form.getInputProps("last_name")}
          />

          <TextInput
            label="Email"
            placeholder="john@example.com"
            withAsterisk
            {...form.getInputProps("email")}
          />

          <TextInput
            label="Phone"
            placeholder="9876543210"
            withAsterisk
            {...form.getInputProps("phone")}
          />

          <PasswordInput
            label="Password"
            placeholder="Minimum 8 characters"
            withAsterisk
            {...form.getInputProps("password")}
          />

          <PasswordInput
            label="Confirm Password"
            placeholder="Enter password again"
            withAsterisk
            {...form.getInputProps(
              "confirm_password",
            )}
          />

          <Select
            label="Account Type"
            placeholder="Select account type"
            withAsterisk
            data={[
              {
                value: "CUSTOMER",
                label: "Customer",
              },
              {
                value: "RESTAURANT_OWNER",
                label: "Restaurant Owner",
              },
            ]}
            {...form.getInputProps("role")}
          />

          <Button
            type="submit"
            loading={registerMutation.isPending}
            fullWidth
          >
            Create Account
          </Button>

          <Text
            size="sm"
            ta="center"
          >
            Already have an account?{" "}
            <Anchor
              component={Link}
              to="/login"
            >
              Login
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Paper>
  );
}