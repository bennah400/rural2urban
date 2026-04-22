import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],
      totalItems: 0,
      totalPrice: 0,

      // Add item to cart (or increase quantity if already exists)
      addItem: (product, quantity = 1) => {
        const currentItems = get().items;
        const existingIndex = currentItems.findIndex(item => item.product.id === product.id);

        let newItems;
        if (existingIndex >= 0) {
          newItems = [...currentItems];
          newItems[existingIndex].quantity += quantity;
        } else {
          newItems = [...currentItems, { product, quantity }];
        }

        set({ items: newItems });
        get().recalculateTotals();
      },

      // Remove item completely from cart
      removeItem: (productId) => {
        const newItems = get().items.filter(item => item.product.id !== productId);
        set({ items: newItems });
        get().recalculateTotals();
      },

      // Update quantity of a specific item (min 1, max stock)
      updateQuantity: (productId, quantity) => {
        const newItems = get().items.map(item =>
          item.product.id === productId
            ? { ...item, quantity: Math.max(1, Math.min(quantity, item.product.stock_quantity)) }
            : item
        );
        set({ items: newItems });
        get().recalculateTotals();
      },

      // Clear entire cart
      clearCart: () => {
        set({ items: [], totalItems: 0, totalPrice: 0 });
      },

      // Recalculate totals
      recalculateTotals: () => {
        const items = get().items;
        const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
        const totalPrice = items.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
        set({ totalItems, totalPrice });
      },
    }),
    {
      name: 'cart-storage', // key in localStorage
      getStorage: () => localStorage,
    }
  )
);

export default useCartStore;