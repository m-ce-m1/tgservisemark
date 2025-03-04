import React, { useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import SearchBar from '../components/SearchBar';
import PromoBanner from '../components/PromoBanner';
import ProductGrid from '../components/ProductGrid';
import TelegramLogin from '../components/TelegramLogin';
import { useUser } from '../context/UserContext';

const HomePage: React.FC = () => {
  const { user, addSubscription } = useUser();

  // Handle purchase from Telegram bot
  useEffect(() => {
    // Listen for messages from Telegram WebApp
    const handleTelegramWebAppMessage = (event: MessageEvent) => {
      try {
        if (event.data && typeof event.data === 'string' && event.data.startsWith('tgWebAppData:')) {
          const data = JSON.parse(event.data.substring('tgWebAppData:'.length));
          
          if (data.subscription_type && data.duration) {
            // Process subscription purchase
            addSubscription(data.subscription_type, data.duration);
            
            // Notify Telegram WebApp that purchase was successful
            if (window.Telegram && window.Telegram.WebApp) {
              window.Telegram.WebApp.sendData(JSON.stringify({
                status: 'success',
                subscription_type: data.subscription_type,
                duration: data.duration
              }));
            }
          }
        }
      } catch (error) {
        console.error('Error processing Telegram WebApp message:', error);
      }
    };

    window.addEventListener('message', handleTelegramWebAppMessage);
    
    return () => {
      window.removeEventListener('message', handleTelegramWebAppMessage);
    };
  }, [addSubscription]);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-dark-purple to-black">
      <Header />
      <SearchBar />
      
      {!user?.isAuthenticated && <TelegramLogin />}
      
      <PromoBanner />
      <ProductGrid />
      <Footer />
    </div>
  );
};

export default HomePage;