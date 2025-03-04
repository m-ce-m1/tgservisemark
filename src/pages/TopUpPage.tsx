import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useUser } from '../context/UserContext';
import { ExternalLink } from 'lucide-react';

const TopUpPage: React.FC = () => {
  const { user } = useUser();
  const [telegramBotUrl, setTelegramBotUrl] = useState<string>('');

  useEffect(() => {
    // Получаем имя бота из переменных окружения или используем значение по умолчанию
    const botUsername = process.env.TELEGRAM_BOT_USERNAME || 'YourBotName';
    setTelegramBotUrl(`https://t.me/${botUsername}?start=donate`);
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-dark-purple to-black">
      <Header />
      
      <div className="flex-1 p-4 pb-20">
        <h1 className="text-2xl font-bold mb-6 text-center">Пополнение баланса</h1>
        
        <div className="bg-gray-900 border border-purple-900 rounded-lg p-6">
          <div className="text-center mb-6">
            <div className="text-5xl font-bold mb-2">{user?.balance || 0} ⭐</div>
            <div className="text-gray-400">≈ {((user?.balance || 0) / 50).toFixed(2)}$</div>
          </div>
          
          <div className="mb-6">
            <h2 className="text-xl font-bold mb-3">Как пополнить баланс?</h2>
            <p className="text-gray-300 mb-4">
              Пополнение баланса осуществляется через нашего Telegram бота. Для пополнения:
            </p>
            <ol className="list-decimal pl-5 space-y-2 text-gray-300">
              <li>Перейдите в наш Telegram бот</li>
              <li>Используйте команду /donate</li>
              <li>Укажите желаемую сумму пополнения (от 100 до 10000 звезд)</li>
              <li>Следуйте инструкциям для оплаты</li>
            </ol>
          </div>
          
          <div className="mb-6">
            <h2 className="text-xl font-bold mb-3">Курс обмена</h2>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-2xl font-bold">50 ⭐</div>
                  <div className="text-gray-400">звезд</div>
                </div>
                <div className="text-xl">=</div>
                <div>
                  <div className="text-2xl font-bold">1$</div>
                  <div className="text-gray-400">доллар</div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mb-6">
            <h2 className="text-xl font-bold mb-3">Популярные суммы</h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-gray-800 p-3 rounded-lg text-center">
                <div className="text-xl font-bold">500 ⭐</div>
                <div className="text-gray-400">10$</div>
              </div>
              <div className="bg-gray-800 p-3 rounded-lg text-center">
                <div className="text-xl font-bold">1000 ⭐</div>
                <div className="text-gray-400">20$</div>
              </div>
              <div className="bg-gray-800 p-3 rounded-lg text-center">
                <div className="text-xl font-bold">2500 ⭐</div>
                <div className="text-gray-400">50$</div>
              </div>
              <div className="bg-gray-800 p-3 rounded-lg text-center">
                <div className="text-xl font-bold">5000 ⭐</div>
                <div className="text-gray-400">100$</div>
              </div>
            </div>
          </div>
          
          <a 
            href={telegramBotUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="w-full bg-neon-purple hover:bg-purple-700 text-white py-3 px-4 rounded-lg font-medium flex items-center justify-center transition-colors"
          >
            Перейти к пополнению <ExternalLink size={18} className="ml-2" />
          </a>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default TopUpPage;