import React from 'react';
import { User, Plus, Copy } from 'lucide-react';
import { useUser } from '../context/UserContext';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  const { user } = useUser();

  const handleCopyId = () => {
    if (user?.id) {
      navigator.clipboard.writeText(user.id);
      alert('ID скопирован в буфер обмена');
    }
  };

  const handleTopUp = () => {
    // Открываем Telegram бота для пополнения баланса
    window.open(`https://t.me/${process.env.TELEGRAM_BOT_USERNAME || 'YourBotName'}?start=topup`, '_blank');
  };

  return (
    <div className="flex justify-between items-center p-4 bg-dark-purple border-b border-purple-900">
      <div className="flex items-center gap-2">
        <div className="bg-neon-purple rounded-lg p-2">
          <User size={24} />
        </div>
        <div>
          <div className="font-bold">{user?.name || 'Гость'}</div>
          <div className="text-xs text-gray-400">ID: {user?.id || 'Не авторизован'}</div>
        </div>
        {user?.id && (
          <button className="ml-1" onClick={handleCopyId}>
            <Copy size={16} className="text-gray-400" />
          </button>
        )}
      </div>
      <div className="flex items-center gap-2">
        <div>
          <div className="text-xs text-gray-400">Баланс:</div>
          <div className="font-bold">{user?.balance || 0} ⭐</div>
        </div>
        <button 
          onClick={handleTopUp} 
          className="bg-neon-purple rounded-lg p-2"
        >
          <Plus size={20} />
        </button>
      </div>
    </div>
  );
};

export default Header;