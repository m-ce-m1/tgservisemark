import React, { useEffect } from 'react';
import { useUser } from '../context/UserContext';

interface TelegramUser {
  id: string;
  first_name: string;
  username?: string;
  photo_url?: string;
  auth_date: number;
  hash: string;
}

declare global {
  interface Window {
    TelegramLoginWidget: {
      dataOnauth: (user: TelegramUser) => void;
    };
  }
}

const TelegramLogin: React.FC = () => {
  const { login } = useUser();

  useEffect(() => {
    // Create script element for Telegram Login Widget
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.setAttribute('data-telegram-login', 'YourBotName'); // Replace with your bot name
    script.setAttribute('data-size', 'large');
    script.setAttribute('data-radius', '8');
    script.setAttribute('data-request-access', 'write');
    script.setAttribute('data-userpic', 'false');
    script.setAttribute('data-auth-url', window.location.href);
    script.async = true;

    // Handle Telegram login callback
    window.TelegramLoginWidget = {
      dataOnauth: (user: TelegramUser) => {
        // Register user in the database
        registerUserInDatabase(user);
        login(user);
      }
    };

    // Add script to the container
    const container = document.getElementById('telegram-login-container');
    if (container) {
      container.appendChild(script);
    }

    return () => {
      // Clean up
      if (container && container.contains(script)) {
        container.removeChild(script);
      }
    };
  }, [login]);

  // Function to register user in the database
  const registerUserInDatabase = async (user: TelegramUser) => {
    try {
      // Get current date
      const currentDate = new Date().toISOString();
      
      // Send user data to the server
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          website_reg_date: currentDate,
          telegram_data: {
            first_name: user.first_name,
            username: user.username,
            auth_date: user.auth_date
          }
        }),
      });
      
      if (!response.ok) {
        console.error('Failed to register user in database');
      }
    } catch (error) {
      console.error('Error registering user:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-gray-900 mx-4 rounded-lg border border-purple-900 mb-4">
      <h2 className="text-xl font-bold mb-4">Войти через Telegram</h2>
      <div id="telegram-login-container" className="mb-4"></div>
      <p className="text-sm text-gray-400 text-center">
        Авторизуйтесь через Telegram для доступа к полному функционалу сайта
      </p>
    </div>
  );
};

export default TelegramLogin;