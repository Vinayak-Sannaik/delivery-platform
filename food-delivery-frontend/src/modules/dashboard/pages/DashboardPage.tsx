import { Button, Card, Stack, Title } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../auth/store/auth.store";

export default function DashboardPage() {
  const navigate = useNavigate();

  const user = useAuthStore(
  (state) => state.user
);

  return (
    <Stack>
      <Title order={2}>Dashboard</Title>

      <Card withBorder>
        <Button fullWidth onClick={() => navigate("/restaurants")}>
          Browse Restaurants
        </Button>
      </Card>

      <Card withBorder>
        <Button fullWidth onClick={() => navigate("/orders")}>
          My Orders
        </Button>
      </Card>

      <Card withBorder>
        <Button fullWidth onClick={() => navigate("/owner/restaurants")}>
          Restaurant Owner
        </Button>
      </Card>
      <Card withBorder>
        <Button onClick={() => navigate("/delivery")}>Delivery Partner</Button>
      </Card>
      <Card withBorder>
        {user?.role === "ADMIN" && (
          <Button onClick={() => navigate("/admin/deliveries")}>
            Manage Deliveries
          </Button>
        )}
      </Card>
    </Stack>
  );
}
