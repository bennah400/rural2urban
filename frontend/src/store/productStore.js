import { create } from 'zustand';
import apiClient from '../services/apiClients';

const useProductStore = create((set, get) => ({
  products: [],
  isLoading: false,
  error: null,
  filters: { search: '', category: '', ordering: '-created_at' },

  fetchProducts: async (params = {}) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/products/', {
        params: { ...get().filters, ...params },
      });
      set({ products: response.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  setFilters: (newFilters) => {
    set((state) => ({ filters: { ...state.filters, ...newFilters } }));
    get().fetchProducts();
  },

  createProduct: async (productData) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.post('/products/', productData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      set((state) => ({ products: [response.data, ...state.products], isLoading: false }));
      return { success: true, data: response.data };
    } catch (error) {
      set({ error: error.response?.data, isLoading: false });
      return { success: false, error: error.response?.data };
    }
  },

  updateProduct: async (id, productData) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.patch(`/products/${id}/`, productData);
      set((state) => ({
        products: state.products.map(p => p.id === id ? response.data : p),
        isLoading: false,
      }));
      return { success: true };
    } catch (error) {
      set({ error: error.response?.data, isLoading: false });
      return { success: false };
    }
  },

  deleteProduct: async (id) => {
    set({ isLoading: true });
    try {
      await apiClient.delete(`/products/${id}/`);
      set((state) => ({
        products: state.products.filter(p => p.id !== id),
        isLoading: false,
      }));
      return { success: true };
    } catch (error) {
      set({ error: error.response?.data, isLoading: false });
      return { success: false };
    }
  },
}));

export default useProductStore;