import { Center, Paper } from "@mantine/core";
import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <Center mih="100vh">
      <Paper
        shadow="md"
        radius="md"
        p="xl"
        w={420}
      >
        <Outlet />
      </Paper>
    </Center>
  );
}