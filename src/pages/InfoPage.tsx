import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

const InfoPage: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-dark-purple to-black">
      <Header />
      
      <div className="flex-1 p-4 pb-20">
        <h1 className="text-2xl font-bold mb-4">Информация</h1>
        
        <div className="bg-gray-900 border border-purple-900 rounded-lg p-4 mb-4">
          <h2 className="text-xl font-bold mb-2">О нас</h2>
          <p className="text-gray-300">
            Мы предлагаем широкий выбор игровых товаров и услуг. Наша цель - обеспечить геймеров качественными продуктами по доступным ценам.
          </p>
        </div>
        
        <div className="bg-gray-900 border border-purple-900 rounded-lg p-4 mb-4">
          <h2 className="text-xl font-bold mb-2">Контакты</h2>
          <p className="text-gray-300">
            Служба поддержки: support@example.com<br />
            Telegram: @support_bot
          </p>
        </div>
        
        <div className="bg-gray-900 border border-purple-900 rounded-lg p-4 mb-4">
          <h2 className="text-xl font-bold mb-2">Правила</h2>
          <p className="text-gray-300">
            Пожалуйста, ознакомьтесь с нашими правилами использования сервиса и политикой возврата перед совершением покупок.
          </p>
        </div>
        
        <div className="bg-gray-900 border border-purple-900 rounded-lg p-4">
          <h2 className="text-xl font-bold mb-2">FAQ</h2>
          <div className="space-y-3">
            <div>
              <h3 className="font-bold text-neon-purple">Как пополнить баланс?</h3>
              <p className="text-gray-300">Нажмите на кнопку "+" рядом с балансом и выберите удобный способ оплаты.</p>
            </div>
            <div>
              <h3 className="font-bold text-neon-purple">Как получить товар после покупки?</h3>
              <p className="text-gray-300">После оплаты вы получите код активации или инструкции по получению товара.</p>
            </div>
            <div>
              <h3 className="font-bold text-neon-purple">Что делать если возникли проблемы?</h3>
              <p className="text-gray-300">Обратитесь в нашу службу поддержки через Telegram или по электронной почте.</p>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default InfoPage;