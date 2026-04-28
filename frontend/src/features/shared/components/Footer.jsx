// src/shared/components/Footer.jsx
export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-2">Rural2City</h3>
            <p className="text-sm text-gray-300">Connecting rural producers with urban markets.</p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Quick Links</h4>
            <ul className="text-sm space-y-1">
              <li><a href="/" className="text-gray-300 hover:text-white">Home</a></li>
              <li><a href="/products" className="text-gray-300 hover:text-white">Products</a></li>
              <li><a href="/about" className="text-gray-300 hover:text-white">About</a></li>
              <li><a href="/contact" className="text-gray-300 hover:text-white">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Contact</h4>
            <p className="text-sm text-gray-300">Email: info@rural2city.com</p>
            <p className="text-sm text-gray-300">Phone: +254 700 123456</p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-6 pt-4 text-center text-sm text-gray-400">
          &copy; {new Date().getFullYear()} Rural2City. All rights reserved.
        </div>
      </div>
    </footer>
  );
}