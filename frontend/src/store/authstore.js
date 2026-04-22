import { create } from 'zustand';
import apiClient from '../services/apiClients';

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  register: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/users/register/', userData);
      const { access, refresh, user } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      set({ user, isAuthenticated: true, isLoading: false });
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.message || 'Registration failed';
      set({ error: message, isLoading: false });
      return { success: false, error: message };
    }
  },

  login: async (phone_number, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/users/login/', { phone_number, password });
      const { access, refresh, user } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      set({ user, isAuthenticated: true, isLoading: false });
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.non_field_errors?.[0] || 'Invalid credentials';
      set({ error: message, isLoading: false });
      return { success: false, error: message };
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, isAuthenticated: false, error: null });
  },

  loadUser: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    set({ isLoading: true });
    try {
      const response = await apiClient.get('/users/me/');
      set({ user: response.data, isAuthenticated: true, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
    }
  },
}));

export default useAuthStore;