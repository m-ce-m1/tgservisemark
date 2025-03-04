import React, { useState } from 'react';
import ProductCard from './ProductCard';

const products = [
  // Полные подписки
  {
    id: 1,
    title: 'Полная подписка на 1 месяц',
    image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 7,
    isNew: true,
    platform: 'Все платформы',
    discount: null,
    category: 'full'
  },
  {
    id: 2,
    title: 'Полная подписка на 3 месяца',
    image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 18,
    isNew: true,
    platform: 'Все платформы',
    discount: 21,
    category: 'full'
  },
  {
    id: 3,
    title: 'Полная подписка на 6 месяцев',
    image: 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 30,
    isNew: true,
    platform: 'Все платформы',
    discount: 42,
    category: 'full'
  },
  {
    id: 4,
    title: 'Полная подписка на 1 год',
    image: 'https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 55,
    isNew: true,
    platform: 'Все платформы',
    discount: 82,
    category: 'full'
  },
  
  // Базовые подписки
  {
    id: 5,
    title: 'Подписка на 1 месяц',
    image: 'https://images.unsplash.com/photo-1511512578047-dfb367046420?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 5,
    isNew: true,
    platform: 'Базовая',
    discount: null,
    category: 'basic'
  },
  {
    id: 6,
    title: 'Подписка на 3 месяца',
    image: 'https://images.unsplash.com/photo-1586182987320-4f17e36750df?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 13,
    isNew: true,
    platform: 'Базовая',
    discount: 15,
    category: 'basic'
  },
  {
    id: 7,
    title: 'Подписка на 6 месяцев',
    image: 'https://images.unsplash.com/photo-1605899435973-ca2d1a8431cf?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 24,
    isNew: true,
    platform: 'Базовая',
    discount: 30,
    category: 'basic'
  },
  {
    id: 8,
    title: 'Подписка на 1 год',
    image: 'https://images.unsplash.com/photo-1621259182978-fbf93132d53d?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 40,
    isNew: true,
    platform: 'Базовая',
    discount: 60,
    category: 'basic'
  },
  
  // Отключение рекламы
  {
    id: 9,
    title: 'Отключить рекламу во всех ботах на 1 месяц',
    image: 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 2,
    isNew: true,
    platform: 'Все боты',
    discount: null,
    category: 'adblock'
  },
  {
    id: 10,
    title: 'Отключить подписку на 3 месяца',
    image: 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 4,
    isNew: true,
    platform: 'Все боты',
    discount: 6,
    category: 'adblock'
  },
  {
    id: 11,
    title: 'Отключить подписку на 6 месяцев',
    image: 'https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 6,
    isNew: true,
    platform: 'Все боты',
    discount: 12,
    category: 'adblock'
  },
  {
    id: 12,
    title: 'Отключить рекламу на всегда',
    image: 'https://images.unsplash.com/photo-1633265486064-086b219458ec?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80',
    price: 20,
    isNew: true,
    platform: 'Все боты',
    discount: null,
    category: 'adblock'
  }
];

const ProductGrid: React.FC = () => {
  const [filter, setFilter] = useState<string>('all');
  
  const filteredProducts = filter === 'all' 
    ? products 
    : products.filter(product => product.category === filter);
  
  const categories = [
    { id: 'all', name: 'Все' },
    { id: 'full', name: 'Полные подписки' },
    { id: 'basic', name: 'Базовые подписки' },
    { id: 'adblock', name: 'Отключение рекламы' }
  ];

  return (
    <div className="px-4 pb-20">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Подписки</h2>
        <div className="flex items-center">
          <span className="text-sm text-gray-400 mr-2">Фильтры:</span>
          <select 
            className="bg-dark-purple border border-purple-800 rounded text-sm p-1"
            onChange={(e) => setFilter(e.target.value)}
            value={filter}
          >
            <option value="all">По популярности</option>
            <option value="all">По цене</option>
            <option value="all">По длительности</option>
          </select>
        </div>
      </div>
      
      <div className="flex overflow-x-auto space-x-2 mb-4 pb-2 scrollbar-hide">
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => setFilter(category.id)}
            className={`px-4 py-2 rounded-full whitespace-nowrap ${
              filter === category.id 
                ? 'bg-neon-purple text-white' 
                : 'bg-gray-800 text-gray-300'
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>
      
      {filter === 'all' && (
        <>
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-3 text-neon-purple">Полные подписки</h3>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
              {products.filter(p => p.category === 'full').map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-3 text-neon-purple">Базовые подписки</h3>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
              {products.filter(p => p.category === 'basic').map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-3 text-neon-purple">Отключение рекламы</h3>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
              {products.filter(p => p.category === 'adblock').map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        </>
      )}
      
      {filter !== 'all' && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
          {filteredProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductGrid;