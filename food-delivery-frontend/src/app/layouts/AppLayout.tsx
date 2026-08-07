import { AppShell } from "@mantine/core";
import { Outlet } from "react-router-dom";

import AppHeader from "../../shared/components/AppHeader";
import AppSidebar from "../../shared/components/AppSidebar";

import { useUIStore } from "../../shared/store/ui.store";

export default function AppLayout() {
  const sidebarOpened = useUIStore(
    (state) => state.sidebarOpened
  );

  return (
    <AppShell
      header={{
        height: 70,
      }}
      navbar={{
        width: 260,
        breakpoint: "md",
        collapsed: {
          mobile: !sidebarOpened,
        },
      }}
      padding="md"
    >
      <AppShell.Header>
        <AppHeader />
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <AppSidebar />
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}