// src/shared/components/Navbar.jsx
import { Link } from 'react-router-dom';
import useAuthStore from '../../store/authstore';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <nav className="bg-green-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">Rural2City</Link>
        <div className="flex items-center space-x-4">
          <Link to="/products" className="hover:text-green-200">Products</Link>
          {isAuthenticated ? (
            <>
              <Link to="/cart" className="hover:text-green-200">Cart</Link>
              {user?.user_type === 'producer' && (
                <Link to="/dashboard" className="hover:text-green-200">Dashboard</Link>
              )}
              <button onClick={logout} className="bg-red-500 px-3 py-1 rounded hover:bg-red-600">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-green-200">Login</Link>
              <Link to="/register" className="bg-yellow-500 px-3 py-1 rounded hover:bg-yellow-600">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}