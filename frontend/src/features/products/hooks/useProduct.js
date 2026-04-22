import { useEffect } from 'react';
import useProductStore from '../../../store/productStore';

const useProduct = (productId = null) => {
  const {
    products,
    isLoading,
    error,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    filters,
    setFilters,
  } = useProductStore();

  useEffect(() => {
    if (products.length === 0) {
      fetchProducts();
    }
  }, []);

  const product = productId
    ? products.find(p => p.id === parseInt(productId))
    : null;

  return {
    products,
    product,
    isLoading,
    error,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    filters,
    setFilters,
  };
};

export default useProduct;