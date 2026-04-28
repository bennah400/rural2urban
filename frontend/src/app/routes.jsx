import { Routes, Route } from 'react-router-dom';
import ProductListPage from '../features/products/pages/ProductListPage';
import LoginPage from '../features/auth/pages/LoginPage';
import RegisterPage from '../features/auth/pages/RegisterPage';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ProductListPage />} />
      <Route path="/products" element={<ProductListPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>
  );
}