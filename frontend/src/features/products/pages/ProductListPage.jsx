import { useEffect, useState } from 'react';
import useProductStore from '../../../store/productStore'; // adjust path if needed
import useCartStore from '../../../store/cartStore.js';
import useAuthStore from '../../../store/authstore.js';
import { formatKES } from '../../../shared/utils/formatKES';

export default function ProductListPage() {
  const { products, fetchProducts, filters, setFilters, isLoading } = useProductStore();
  const { addItem } = useCartStore();
  const { isAuthenticated, user } = useAuthStore();
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSearch = () => {
    setFilters({ search: searchTerm });
  };

  const handleAddToCart = (product) => {
    if (product.stock_quantity <= 0) {
      alert('Out of stock');
      return;
    }
    addItem(product, 1);
    alert(`${product.name} added to cart`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">All Products</h1>
        {isAuthenticated && user?.user_type === 'producer' && (
          <a
            href="/products/create"
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            + Add Product
          </a>
        )}
      </div>

      {/* Search & filter bar */}
      <div className="mb-6 flex flex-wrap gap-2">
        <input
          type="text"
          placeholder="Search products..."
          className="border p-2 rounded flex-1 min-w-[200px]"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Search
        </button>
        <select
          onChange={(e) => setFilters({ category: e.target.value })}
          className="border p-2 rounded"
        >
          <option value="">All Categories</option>
          <option value="Vegetables">Vegetables</option>
          <option value="Fruits">Fruits</option>
          <option value="Grains">Grains</option>
        </select>
        <select
          onChange={(e) => setFilters({ ordering: e.target.value })}
          className="border p-2 rounded"
        >
          <option value="-created_at">Newest First</option>
          <option value="price">Price: Low to High</option>
          <option value="-price">Price: High to Low</option>
          <option value="name">Name A-Z</option>
        </select>
      </div>

      {/* Loading state */}
      {isLoading && <p className="text-center">Loading products...</p>}

      {/* Product grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.id} className="border rounded-lg shadow-md overflow-hidden bg-white">
            {product.image && (
              <img
                src={`http://localhost:8000${product.image}`}
                alt={product.name}
                className="w-full h-48 object-cover"
              />
            )}
            <div className="p-4">
              <h2 className="text-xl font-semibold">{product.name}</h2>
              <p className="text-gray-600 text-sm mt-1">{product.description.substring(0, 100)}</p>
              <div className="mt-3 flex justify-between items-center">
                <span className="text-lg font-bold text-green-700">{formatKES(product.price)}</span>
                <span className="text-sm text-gray-500">Stock: {product.stock_quantity}</span>
              </div>
              <button
                onClick={() => handleAddToCart(product)}
                disabled={product.stock_quantity <= 0}
                className={`mt-4 w-full py-2 rounded transition ${
                  product.stock_quantity > 0
                    ? 'bg-yellow-500 hover:bg-yellow-600 text-white'
                    : 'bg-gray-300 cursor-not-allowed'
                }`}
              >
                {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {!isLoading && products.length === 0 && (
        <p className="text-center text-gray-500 mt-10">No products found.</p>
      )}
    </div>
  );
}