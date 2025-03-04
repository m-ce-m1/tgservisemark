import React from 'react';
import { ChevronRight, Gift, Zap } from 'lucide-react';

const PromoBanner: React.FC = () => {
  return (
    <div className="px-4 space-y-3 my-4">
      <div className="bg-gradient-to-r from-purple-900 to-indigo-800 rounded-lg p-4 flex justify-between items-center shadow-lg shadow-purple-900/20">
        <div className="flex items-center">
          <div className="mr-3">
            <Zap className="text-purple-400" size={24} />
          </div>
          <span className="text-lg font-bold uppercase tracking-wider">СПЕЦ. ПРЕДЛОЖЕНИЯ</span>
        </div>
        <ChevronRight className="text-purple-400" size={24} />
      </div>
      
      <div className="bg-gradient-to-r from-neon-purple to-purple-700 rounded-lg p-4 flex justify-between items-center shadow-lg shadow-purple-900/20">
        <div className="flex items-center">
          <div className="mr-3">
            <Gift className="text-white" size={24} />
          </div>
          <span className="text-lg font-bold uppercase tracking-wider">ПОЛУЧИТЬ БОНУС</span>
        </div>
        <ChevronRight className="text-white" size={24} />
      </div>
    </div>
  );
};

export default PromoBanner;