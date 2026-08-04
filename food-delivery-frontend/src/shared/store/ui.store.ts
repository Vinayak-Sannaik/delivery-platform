import { create } from "zustand";

interface UIStore {
  sidebarOpened: boolean;

  toggleSidebar: () => void;

  closeSidebar: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpened: true,

  toggleSidebar: () =>
    set((state) => ({
      sidebarOpened: !state.sidebarOpened,
    })),

  closeSidebar: () =>
    set({
      sidebarOpened: false,
    }),
}));