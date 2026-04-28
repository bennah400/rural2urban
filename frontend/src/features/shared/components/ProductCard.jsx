// src/shared/components/ProductCard.jsx
import Card from './Card';
import Button from './Button';
import { formatKES } from '../utils/formatKES';

export default function ProductCard({ product, onAddToCart }) {
  const imageUrl = product.image
    ? `http://localhost:8000${product.image}`
    : 'https://via.placeholder.com/300x200?text=No+Image';

  return (
    <Card className="flex flex-col h-full">
      <img src={imageUrl} alt={product.name} className="w-full h-48 object-cover" />
      <div className="p-4 flex flex-col flex-grow">
        <h3 className="text-lg font-semibold text-gray-800">{product.name}</h3>
        <p className="text-gray-600 text-sm mt-1 line-clamp-2">{product.description}</p>
        <div className="mt-3 flex justify-between items-center">
          <span className="text-xl font-bold text-green-700">{formatKES(product.price)}</span>
          <span className="text-sm text-gray-500">Stock: {product.stock_quantity}</span>
        </div>
        <div className="mt-4">
          <Button
            onClick={() => onAddToCart(product)}
            disabled={product.stock_quantity <= 0}
            variant="primary"
            fullWidth
          >
            {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
          </Button>
        </div>
      </div>
    </Card>
  );
}