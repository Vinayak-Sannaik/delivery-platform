
import {
  ActionIcon,
  Avatar,
  Burger,
  Group,
  Indicator,
  Menu,
  Text,
  UnstyledButton,
} from "@mantine/core";

import {
  IconLogout,
  IconShoppingCart,
  IconUser,
} from "@tabler/icons-react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import { useUIStore } from "../../store/ui.store";
import { useCartStore } from "../../../modules/cart/store/cart.store";
import { useAuthStore } from "../../../modules/auth/store/auth.store";

export default function AppHeader() {
  const { sidebarOpened, toggleSidebar } =
    useUIStore();

  const items = useCartStore(
    (state) => state.items
  );

  const user = useAuthStore(
    (state) => state.user
  );

  const logout = useAuthStore(
    (state) => state.logout
  );

  const navigate = useNavigate();

  const totalItems = items.reduce(
    (sum, item) => sum + item.quantity,
    0
  );

  const handleLogout = () => {
    logout();

    navigate("/login", {
      replace: true,
    });
  };

  const userInitial =
    user?.email?.charAt(0).toUpperCase() ?? "U";

  return (
    <Group
      justify="space-between"
      h="100%"
      px="md"
    >
      {/* Left */}
      <Group>
        <Burger
          opened={sidebarOpened}
          onClick={toggleSidebar}
        />

        <Text fw={700}>
          Food Delivery Platform
        </Text>
      </Group>

      {/* Right */}
      <Group gap="md">
        {/* Cart */}
        <Indicator
          inline
          label={totalItems}
          size={16}
          disabled={totalItems === 0}
        >
          <ActionIcon
            component={Link}
            to="/cart"
            variant="subtle"
            size="lg"
            aria-label="Cart"
          >
            <IconShoppingCart size={24} />
          </ActionIcon>
        </Indicator>

        {/* User Menu */}
        <Menu
          shadow="md"
          width={220}
          position="bottom-end"
        >
          <Menu.Target>
            <UnstyledButton>
              <Avatar
                radius="xl"
                color="blue"
              >
                {userInitial}
              </Avatar>
            </UnstyledButton>
          </Menu.Target>

          <Menu.Dropdown>
            {/* User information */}
            <Menu.Label>
              Account
            </Menu.Label>

            <Menu.Item
              leftSection={
                <IconUser size={16} />
              }
              disabled
            >
              <div>
                <Text size="sm" fw={500}>
                  {user?.email ?? "User"}
                </Text>

                <Text
                  size="xs"
                  c="dimmed"
                >
                  {user?.role ?? ""}
                </Text>
              </div>
            </Menu.Item>

            <Menu.Divider />

            {/* Profile */}
            <Menu.Item
              leftSection={
                <IconUser size={16} />
              }
              onClick={() =>
                navigate("/profile")
              }
            >
              Profile
            </Menu.Item>

            <Menu.Divider />

            {/* Logout */}
            <Menu.Item
              color="red"
              leftSection={
                <IconLogout size={16} />
              }
              onClick={handleLogout}
            >
              Logout
            </Menu.Item>
          </Menu.Dropdown>
        </Menu>
      </Group>
    </Group>
  );
}
