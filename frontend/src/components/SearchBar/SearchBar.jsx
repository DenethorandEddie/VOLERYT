import React, { useState } from 'react';
import './SearchBar.css';

const SearchBar = ({ onSearch, loading }) => {
  const [niche, setNiche] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (niche.trim()) {
      onSearch(niche.trim());
    }
  };

  return (
    <div className="search-bar-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder="Enter niche keyword (e.g., basketball highlights, cooking tutorials)"
            value={niche}
            onChange={(e) => setNiche(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            className="search-button"
            disabled={loading || !niche.trim()}
          >
            {loading ? 'Searching...' : 'Search Niche'}
          </button>
        </div>
        <p className="search-hint">
          Search for a specific niche to analyze competition and find opportunities
        </p>
      </form>
    </div>
  );
};

export default SearchBar;
