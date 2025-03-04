import React, { createContext, useState, useContext, ReactNode } from 'react';

interface User {
  id: string;
  name: string;
  balance: number;
  isAuthenticated: boolean;
}

interface Subscription {
  type: string;
  duration: number;
  endDate: string | null;
}

interface UserContextType {
  user: User | null;
  subscriptions: Subscription[];
  login: (userData: any) => void;
  logout: () => void;
  updateBalance: (amount: number) => void;
  addSubscription: (type: string, duration: number) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);

  const login = (userData: any) => {
    setUser({
      id: userData.id || userData.user_id,
      name: userData.first_name || 'User',
      balance: 0,
      isAuthenticated: true,
    });
    
    // Fetch user subscriptions from the server
    fetchUserSubscriptions(userData.id || userData.user_id);
  };

  const logout = () => {
    setUser(null);
    setSubscriptions([]);
  };

  const updateBalance = (amount: number) => {
    if (user) {
      setUser({
        ...user,
        balance: user.balance + amount,
      });
    }
  };

  const addSubscription = async (type: string, duration: number) => {
    if (!user) return;
    
    try {
      // Calculate end date
      const endDate = duration > 0 
        ? new Date(Date.now() + duration * 30 * 24 * 60 * 60 * 1000).toISOString()
        : null;
      
      // Add subscription to state
      setSubscriptions([
        ...subscriptions,
        { type, duration, endDate }
      ]);
      
      // Send subscription to server
      await fetch('/api/subscription', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          subscription_type: type,
          duration: duration
        }),
      });
      
    } catch (error) {
      console.error('Error adding subscription:', error);
    }
  };

  const fetchUserSubscriptions = async (userId: string) => {
    try {
      const response = await fetch(`/api/user/${userId}`);
      
      if (response.ok) {
        const userData = await response.json();
        
        if (userData.subscriptions) {
          const userSubscriptions: Subscription[] = [];
          
          if (userData.subscriptions.full_subscription > 0) {
            userSubscriptions.push({
              type: 'full',
              duration: userData.subscriptions.full_subscription,
              endDate: userData.subscriptions.full_subscription_end
            });
          }
          
          if (userData.subscriptions.basic_subscription > 0) {
            userSubscriptions.push({
              type: 'basic',
              duration: userData.subscriptions.basic_subscription,
              endDate: userData.subscriptions.basic_subscription_end
            });
          }
          
          if (userData.subscriptions.ad_free > 0) {
            userSubscriptions.push({
              type: 'ad_free',
              duration: userData.subscriptions.ad_free,
              endDate: userData.subscriptions.ad_free_end
            });
          }
          
          setSubscriptions(userSubscriptions);
        }
        
        // Update user balance if available
        if (userData.balance !== undefined) {
          setUser(prevUser => prevUser ? {
            ...prevUser,
            balance: userData.balance
          } : null);
        }
      }
    } catch (error) {
      console.error('Error fetching user subscriptions:', error);
    }
  };

  return (
    <UserContext.Provider value={{ 
      user, 
      subscriptions, 
      login, 
      logout, 
      updateBalance, 
      addSubscription 
    }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};