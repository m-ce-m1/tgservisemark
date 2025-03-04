import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CartPage from './pages/CartPage';
import InfoPage from './pages/InfoPage';
import TopUpPage from './pages/TopUpPage';
import { UserProvider } from './context/UserContext';

function App() {
  return (
    <UserProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-b from-dark-purple to-black text-white">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/info" element={<InfoPage />} />
            <Route path="/topup" element={<TopUpPage />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;