import {
  Button,
  Paper,
  PasswordInput,
  Stack,
  TextInput,
  Title,
  Text,
  Anchor,
} from "@mantine/core";

import { useForm } from "@mantine/form";
import { useNavigate, Link } from "react-router-dom";

import { useLogin } from "../hooks/useLogin";
import { useAuthStore } from "../store/auth.store";

export default function LoginPage() {
  const navigate = useNavigate();

  const form = useForm({
    initialValues: {
      email: "",
      password: "",
    },
  });

  const loginMutation = useLogin();

  const handleSubmit = form.onSubmit(
    async (values) => {
      try {
        await loginMutation.mutateAsync(values);

        const user =
          useAuthStore.getState().user;

        if (!user) {
          throw new Error(
            "User information was not loaded after login."
          );
        }

        switch (user.role) {
          case "CUSTOMER":
            navigate("/restaurants", {
              replace: true,
            });
            break;

          case "RESTAURANT_OWNER":
            navigate("/owner/restaurants", {
              replace: true,
            });
            break;

          case "ADMIN":
            navigate("/admin/deliveries", {
              replace: true,
            });
            break;

          case "DELIVERY_PARTNER":
            navigate("/delivery", {
              replace: true,
            });
            break;

          default:
            navigate("/dashboard", {
              replace: true,
            });
        }
      } catch (error) {
        console.error(
          "Login failed:",
          error
        );
      }
    }
  );

  return (
    <Paper
      withBorder
      shadow="sm"
      p="xl"
      radius="md"
      maw={420}
      mx="auto"
      mt={80}
    >
      <form onSubmit={handleSubmit}>
        <Stack>
          <Title order={2}>
            Sign in
          </Title>

          <Text c="dimmed" size="sm">
            Sign in to your account to continue.
          </Text>

          <TextInput
            label="Email"
            placeholder="Enter your email"
            type="email"
            required
            {...form.getInputProps("email")}
          />

          <PasswordInput
            label="Password"
            placeholder="Enter your password"
            required
            {...form.getInputProps("password")}
          />

          <Button
            type="submit"
            loading={loginMutation.isPending}
            fullWidth
          >
            Sign in
          </Button>
          <Text
            size="sm"
            ta="center"
          >
            Not have an account?{" "}
            <Anchor
              component={Link}
              to="/register"
            >
              Register
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Paper>
  );
}