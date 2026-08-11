import {
  IconLayoutDashboard,
  IconBuildingStore,
  IconClipboardList,
  IconTruckDelivery,
  // IconActivity,
  // IconSettings,
} from "@tabler/icons-react";

import type { TablerIcon } from "@tabler/icons-react";
import { UserRole } from "../../app/router/route.types";

export interface NavigationItem {
  label: string;
  path: string;
  icon: TablerIcon;
  roles: UserRole[];
}

export const navigation: NavigationItem[] = [
  {
    label: "Dashboard",
    path: "/dashboard",
    icon: IconLayoutDashboard,
    roles: [
      UserRole.ADMIN,
      UserRole.RESTAURANT_OWNER,
      UserRole.DELIVERY_PARTNER,
    ],
  },

  {
    label: "Restaurants",
    path: "/restaurants",
    icon: IconBuildingStore,
    roles: [UserRole.CUSTOMER],
  },

  {
    label: "Orders",
    path: "/orders",
    icon: IconClipboardList,
    roles: [
      UserRole.CUSTOMER,
      UserRole.RESTAURANT_OWNER,
    ],
  },

  {
    label: "Delivery",
    path: "/delivery",
    icon: IconTruckDelivery,
    roles: [UserRole.DELIVERY_PARTNER],
  },

  // {
  //   label: "System Health",
  //   path: "/health",
  //   icon: IconActivity,
  //   roles: [UserRole.ADMIN],
  // },

  // {
  //   label: "Settings",
  //   path: "/settings",
  //   icon: IconSettings,
  //   roles: [
  //     UserRole.ADMIN,
  //     UserRole.CUSTOMER,
  //     UserRole.RESTAURANT_OWNER,
  //     UserRole.DELIVERY_PARTNER,
  //   ],
  // },
];