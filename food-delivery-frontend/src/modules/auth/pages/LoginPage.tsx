import { Button, Paper, PasswordInput, Stack, TextInput, Title } from "@mantine/core";
import { useForm } from "@mantine/form";

import { useLogin } from "../hooks/useLogin";

export default function LoginPage() {
  const form = useForm({
    initialValues: {
      email: "",
      password: "",
    },
  });

  const loginMutation = useLogin();

  const handleSubmit = form.onSubmit(async (values) => {
    try {
      const response = await loginMutation.mutateAsync(values);

      console.log("Login Success:", response);
    } catch (error) {
      console.error("Login Failed:", error);
    }
  });

  return (
    <Paper>
      <form onSubmit={handleSubmit}>
        <Stack>
          <Title order={2}>Login</Title>

          <TextInput
            label="Email"
            placeholder="Enter your email"
            {...form.getInputProps("email")}
          />

          <PasswordInput
            label="Password"
            placeholder="Enter your password"
            {...form.getInputProps("password")}
          />

          <Button
            type="submit"
            loading={loginMutation.isPending}
          >
            Login
          </Button>
        </Stack>
      </form>
    </Paper>
  );
}