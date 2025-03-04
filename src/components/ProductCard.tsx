import React from 'react';
import { useUser } from '../context/UserContext';

interface ProductProps {
  product: {
    id: number;
    title: string;
    image: string;
    price: number;
    isNew: boolean;
    platform: string;
    discount: number | null;
    category?: string;
  };
}

const ProductCard: React.FC<ProductProps> = ({ product }) => {
  const { user, addSubscription } = useUser();

  const handlePurchase = () => {
    if (!user?.isAuthenticated) {
      alert('Пожалуйста, авторизуйтесь через Telegram для совершения покупок');
      return;
    }

    // Determine subscription type and duration based on product
    let subscriptionType = '';
    let duration = 0;

    if (product.category === 'full') {
      subscriptionType = 'full';
      // Determine duration based on product title
      if (product.title.includes('1 месяц')) duration = 1;
      else if (product.title.includes('3 месяца')) duration = 3;
      else if (product.title.includes('6 месяцев')) duration = 6;
      else if (product.title.includes('1 год')) duration = 12;
    } else if (product.category === 'basic') {
      subscriptionType = 'basic';
      if (product.title.includes('1 месяц')) duration = 1;
      else if (product.title.includes('3 месяца')) duration = 3;
      else if (product.title.includes('6 месяцев')) duration = 6;
      else if (product.title.includes('1 год')) duration = 12;
    } else if (product.category === 'adblock') {
      subscriptionType = 'ad_free';
      if (product.title.includes('на всегда')) duration = 0; // Permanent
      else if (product.title.includes('1 месяц')) duration = 1;
      else if (product.title.includes('3 месяца')) duration = 3;
      else if (product.title.includes('6 месяцев')) duration = 6;
    }

    if (subscriptionType && (duration > 0 || subscriptionType === 'ad_free')) {
      // Конвертируем цену в звезды (1$ = 50 звезд)
      const starsPrice = product.price * 50;
      
      // Check if user has enough balance
      if (user.balance < starsPrice) {
        alert(`Недостаточно звезд на балансе. Необходимо: ${starsPrice} звезд. Пожалуйста, пополните баланс.`);
        return;
      }

      // Process purchase
      if (confirm(`Вы уверены, что хотите приобрести "${product.title}" за ${starsPrice} звезд?`)) {
        addSubscription(subscriptionType, duration);
        alert(`Поздравляем! Вы успешно приобрели "${product.title}"`);
      }
    } else {
      alert('Ошибка при обработке покупки. Пожалуйста, попробуйте еще раз.');
    }
  };

  // Конвертируем цену в звезды (1$ = 50 звезд)
  const starsPrice = product.price * 50;
  const discountStarsPrice = product.discount ? product.discount * 50 : null;

  return (
    <div 
      className="bg-gray-900 rounded-lg overflow-hidden border border-purple-900 hover:border-neon-purple transition-all duration-300 hover:shadow-lg hover:shadow-purple-900/30 cursor-pointer"
      onClick={handlePurchase}
    >
      <div className="relative aspect-square">
        <img 
          src={product.image} 
          alt={product.title} 
          className="w-full h-full object-cover"
        />
        {product.isNew && (
          <div className="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded">
            Новинка
          </div>
        )}
      </div>
      <div className="p-2">
        <h3 className="text-sm font-medium truncate">{product.title}</h3>
        <div className="text-xs text-gray-400 mb-2">{product.platform}</div>
        <div className="flex justify-between items-center">
          <span className="text-green-500 font-bold">{starsPrice} ⭐</span>
          {discountStarsPrice && (
            <span className="text-xs text-gray-400 line-through">{discountStarsPrice} ⭐</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;