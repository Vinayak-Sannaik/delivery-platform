import {
  NavLink,
  Stack,
} from "@mantine/core";

import { NavLink as RouterLink } from "react-router-dom";

import { navigation } from "../../constants/navigation";
import { useAuthStore } from "../../../modules/auth/store/auth.store";

export default function AppSidebar() {
  const user = useAuthStore(
    (state) => state.user
  );

  if (!user) {
    return null;
  }

  return (
    <Stack gap={4}>
      {navigation
        .filter((item) =>
          item.roles.includes(user.role)
        )
        .map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              component={RouterLink}
              to={item.path}
              label={item.label}
              leftSection={<Icon size={18} />}
            />
          );
        })}
    </Stack>
  );
}