import React from 'react';
import { Home, ShoppingBag, Info } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Footer: React.FC = () => {
  const location = useLocation();
  
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-dark-purple border-t border-purple-900 flex justify-around py-3">
      <Link to="/" className="flex flex-col items-center">
        <Home size={24} className={location.pathname === '/' ? 'text-neon-purple' : 'text-gray-400'} />
        <span className="text-xs mt-1">Главная</span>
      </Link>
      <Link to="/cart" className="flex flex-col items-center relative">
        <ShoppingBag size={24} className={location.pathname === '/cart' ? 'text-neon-purple' : 'text-gray-400'} />
        <span className="absolute -top-2 -right-2 bg-neon-purple text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">0</span>
        <span className="text-xs mt-1">Корзина</span>
      </Link>
      <Link to="/info" className="flex flex-col items-center">
        <Info size={24} className={location.pathname === '/info' ? 'text-neon-purple' : 'text-gray-400'} />
        <span className="text-xs mt-1">Инфо</span>
      </Link>
    </div>
  );
};

export default Footer;