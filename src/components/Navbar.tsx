import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Twitter } from 'lucide-react';

function Navbar() {
  const location = useLocation();
  
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Twitter className="h-8 w-8 text-blue-500" />
              <span className="text-2xl font-bold text-gray-900">XLENS</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/'
                  ? 'text-blue-600 bg-blue-50'
                  : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              Home
            </Link>
            <Link
              to="/fact-checker"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/fact-checker'
                  ? 'text-blue-600 bg-blue-50'
                  : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              Fact Checker
            </Link>
            <Link
              to="/sentiment"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/sentiment'
                  ? 'text-blue-600 bg-blue-50'
                  : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              Sentiment
            </Link>
            <Link
              to="/viral"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/viral'
                  ? 'text-blue-600 bg-blue-50'
                  : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              Viral Generator
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;