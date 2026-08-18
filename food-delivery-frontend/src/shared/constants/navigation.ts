
import {
  IconHome,
  IconBuildingStore,
  IconTruck,
  IconCategory,
  IconToolsKitchen2,
} from "@tabler/icons-react";

import type { TablerIcon } from "@tabler/icons-react";
import { UserRole } from "../../app/router/route.types";

export interface NavigationItem {
  label: string;
  path: string;
  icon: TablerIcon;
  roles: UserRole[];
}


export const navigation = [
  {
    label: "Dashboard",
    path: "/dashboard",
    icon: IconHome,
    roles: ["CUSTOMER", "RESTAURANT_OWNER", "DELIVERY_PARTNER", "ADMIN"],
  },

  {
    label: "Restaurants",
    path: "/restaurants",
    icon: IconBuildingStore,
    roles: ["CUSTOMER", "RESTAURANT_OWNER", "ADMIN"],
  },

  {
    label: "My Restaurants",
    path: "/owner/restaurants",
    icon: IconBuildingStore,
    roles: ["RESTAURANT_OWNER"],
  },

  {
    label: "Categories",
    path: "/admin/categories",
    icon: IconCategory,
    roles: ["ADMIN"],
  },

  {
    label: "Menu Items",
    path: "/admin/menu-items",
    icon: IconToolsKitchen2,
    roles: ["ADMIN"],
  },

  {
    label: "Manage Restaurants",
    path: "/admin/restaurants",
    icon: IconBuildingStore,
    roles: ["ADMIN"],
  },

  {
    label: "Deliveries",
    path: "/admin/deliveries",
    icon: IconTruck,
    roles: ["ADMIN"],
  },
];