import React from 'react';
import './FilterPanel.css';

const FilterPanel = ({ filters, onFilterChange }) => {
  const handleMaxAgeDaysChange = (e) => {
    onFilterChange('maxAgeDays', parseInt(e.target.value));
  };

  const handleMaxVideosChange = (e) => {
    onFilterChange('maxVideos', parseInt(e.target.value));
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
      </div>

      <div className="filter-info">
        <h4>Niche Criteria:</h4>
        <ul>
          <li>✓ Ideal: ≤5 channels AND ≤50 videos in niche pool</li>
          <li>✓ Good: ≤10 channels AND ≤100 videos in niche pool</li>
          <li>⚠ Channel age calculated from <strong>first upload</strong>, not channel creation</li>
        </ul>
      </div>
    </div>
  );
};

export default FilterPanel;
