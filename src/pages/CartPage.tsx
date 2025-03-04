import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { ShoppingBag } from 'lucide-react';
import { Link } from 'react-router-dom';

const CartPage: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-dark-purple to-black">
      <Header />
      
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        <h1 className="text-2xl font-bold mb-4 text-center">Корзина</h1>
        
        <div className="bg-gray-900 border border-purple-900 rounded-lg p-8 w-full max-w-md flex flex-col items-center">
          <ShoppingBag size={64} className="text-gray-600 mb-4" />
          <p className="text-gray-400 mb-6">Ничего нет :(</p>
          <Link 
            to="/" 
            className="bg-neon-purple text-white py-3 px-6 rounded-lg font-medium w-full text-center hover:bg-purple-700 transition-colors"
          >
            Начать покупки
          </Link>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default CartPage;