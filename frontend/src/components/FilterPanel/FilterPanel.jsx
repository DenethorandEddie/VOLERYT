import React from 'react';
import './FilterPanel.css';

const FilterPanel = ({ filters, onFilterChange }) => {
  const handleMaxAgeDaysChange = (e) => {
    onFilterChange('maxAgeDays', parseInt(e.target.value));
  };

  const handleMaxVideosChange = (e) => {
    onFilterChange('maxVideos', parseInt(e.target.value));
  };

  const handleMinSubscribersChange = (e) => {
    onFilterChange('minSubscribers', parseInt(e.target.value));
  };

  const handleMinTotalViewsChange = (e) => {
    onFilterChange('minTotalViews', parseInt(e.target.value));
  };

  const getAgeTierDescription = (days) => {
    if (days <= 7) return 'S+ Tier (1 week)';
    if (days <= 30) return 'Great (1 month)';
    if (days <= 60) return 'Good (2 months)';
    if (days <= 90) return 'Average (3 months)';
    if (days <= 150) return 'Possible (5 months)';
    return 'Up to 6 months';
  };

  return (
    <div className="filter-panel">
      <h3 className="filter-title">Filters</h3>

      <div className="filter-grid">
        <div className="filter-group">
          <label className="filter-label">
            Maximum Channel Age: {filters.maxAgeDays} days
            <span className="tier-badge">{getAgeTierDescription(filters.maxAgeDays)}</span>
          </label>
          <input
            type="range"
            className="filter-slider"
            min="7"
            max="180"
            step="1"
            value={filters.maxAgeDays}
            onChange={handleMaxAgeDaysChange}
          />
          <div className="slider-labels">
            <span>7 days (S+)</span>
            <span>30 days (Great)</span>
            <span>60 days (Good)</span>
            <span>180 days</span>
          </div>
        </div>

        <div className="filter-group">
          <label className="filter-label">
            Maximum Videos Per Channel: {filters.maxVideos}
          </label>
          <input
            type="range"
            className="filter-slider"
            min="1"
            max="50"
            step="1"
            value={filters.maxVideos}
            onChange={handleMaxVideosChange}
          />
          <div className="slider-labels">
            <span>1</span>
            <span>15 (Ideal)</span>
            <span>50</span>
          </div>
        </div>

        <div className="filter-group">
          <label className="filter-label">
            Minimum Subscribers: {filters.minSubscribers?.toLocaleString() || 0}
          </label>
          <input
            type="range"
            className="filter-slider"
            min="0"
            max="10000"
            step="50"
            value={filters.minSubscribers || 100}
            onChange={handleMinSubscribersChange}
          />
          <div className="slider-labels">
            <span>0</span>
            <span>100 (New)</span>
            <span>1,000</span>
            <span>10,000</span>
          </div>
        </div>

        <div className="filter-group">
          <label className="filter-label">
            Minimum Total Views: {filters.minTotalViews?.toLocaleString() || 0}
          </label>
          <input
            type="range"
            className="filter-slider"
            min="0"
            max="100000"
            step="1000"
            value={filters.minTotalViews || 5000}
            onChange={handleMinTotalViewsChange}
          />
          <div className="slider-labels">
            <span>0</span>
            <span>5K (New)</span>
            <span>25K</span>
            <span>100K</span>
          </div>
        </div>
      </div>

      <div className="filter-info">
        <h4>Discovery Settings:</h4>
        <ul>
          <li>🎯 <strong>New Channels:</strong> 100 subs, 5K views (viral başlangıç)</li>
          <li>✨ <strong>Viral Potential:</strong> Yeni ve hızlı büyüyen kanallar</li>
          <li>🌍 <strong>All Niches:</strong> 30+ farklı kategori taranır</li>
          <li>⚠ Channel age calculated from <strong>first upload</strong></li>
        </ul>
      </div>
    </div>
  );
};

export default FilterPanel;
