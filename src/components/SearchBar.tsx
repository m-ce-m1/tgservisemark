import React from 'react';
import { Search } from 'lucide-react';

const SearchBar: React.FC = () => {
  return (
    <div className="relative mx-4 my-3">
      <input
        type="text"
        placeholder="Искать игру или товар..."
        className="w-full bg-gray-900 border border-purple-900 rounded-lg py-2 pl-10 pr-4 text-white focus:border-neon-purple focus:outline-none focus:ring-1 focus:ring-neon-purple"
      />
      <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
    </div>
  );
};

export default SearchBar;