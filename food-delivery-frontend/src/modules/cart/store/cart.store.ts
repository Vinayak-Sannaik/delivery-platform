import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface CartItem {
  menuItemId: string;
  restaurantId: string;

  name: string;
  price: number;

  quantity: number;
}

interface CartState {
  items: CartItem[];

  addItem: (
    item: Omit<CartItem, "quantity">,
  ) => void;

  removeItem: (
    id: string,
  ) => void;

  increase: (
    id: string,
  ) => void;

  decrease: (
    id: string,
  ) => void;

  clear: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) => {
        const items = [...get().items];

        const existing = items.find(
          (i) => i.menuItemId === item.menuItemId,
        );

        if (existing) {
          existing.quantity += 1;

          set({ items });

          return;
        }

        // Only allow one restaurant in cart
        if (
          items.length > 0 &&
          items[0].restaurantId !== item.restaurantId
        ) {
          set({
            items: [
              {
                ...item,
                quantity: 1,
              },
            ],
          });

          return;
        }

        set({
          items: [
            ...items,
            {
              ...item,
              quantity: 1,
            },
          ],
        });
      },

      removeItem: (id) =>
        set({
          items: get().items.filter(
            (item) => item.menuItemId !== id,
          ),
        }),

      increase: (id) =>
        set({
          items: get().items.map((item) =>
            item.menuItemId === id
              ? {
                  ...item,
                  quantity: item.quantity + 1,
                }
              : item,
          ),
        }),

      decrease: (id) =>
        set({
          items: get()
            .items
            .map((item) =>
              item.menuItemId === id
                ? {
                    ...item,
                    quantity: item.quantity - 1,
                  }
                : item,
            )
            .filter(
              (item) => item.quantity > 0,
            ),
        }),

      clear: () =>
        set({
          items: [],
        }),
    }),
    {
      name: "cart-storage",
    },
  ),
);