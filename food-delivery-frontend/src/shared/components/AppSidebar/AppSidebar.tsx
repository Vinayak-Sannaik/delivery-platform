import {
  NavLink,
  Stack,
} from "@mantine/core";

import { NavLink as RouterLink } from "react-router-dom";

import { navigation } from "../../constants/navigation";
import { UserRole } from "../../../app/router/route.types";

export default function AppSidebar() {
  const role = UserRole.ADMIN;

  return (
    <Stack gap={4}>
      {navigation
        .filter((item) => item.roles.includes(role))
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