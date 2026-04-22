import { create } from 'zustand';
import apiClient from '../services/apiClients';

const useOrderStore = create((set, get) => ({
  orders: [],
  currentOrder: null,
  isLoading: false,
  error: null,

  fetchOrders: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/orders/');
      set({ orders: response.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchOrderDetails: async (orderId) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get(`/orders/${orderId}/`);
      set({ currentOrder: response.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  createOrder: async (orderData) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.post('/orders/', orderData);
      set((state) => ({ orders: [response.data, ...state.orders], isLoading: false }));
      return { success: true, data: response.data };
    } catch (error) {
      set({ error: error.response?.data, isLoading: false });
      return { success: false, error: error.response?.data };
    }
  },

  updateOrderStatus: async (orderId, status) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.patch(`/orders/${orderId}/`, { status });
      set((state) => ({
        orders: state.orders.map(o => o.id === orderId ? response.data : o),
        currentOrder: response.data,
        isLoading: false,
      }));
      return { success: true };
    } catch (error) {
      set({ error: error.message, isLoading: false });
      return { success: false };
    }
  },
}));

export default useOrderStore;