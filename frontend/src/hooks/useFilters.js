import { useState } from 'react';

/**
 * Custom hook for managing filter state
 */
export const useFilters = () => {
  const [filters, setFilters] = useState({
    maxAgeDays: 180,         // 6 months default
    maxVideos: 15,           // 15 videos default
    minSubscribers: 1000,    // Min 1K subscribers
    minTotalViews: 50000,    // Min 50K total views
    maxResults: 50,          // Max channels to analyze
    regionCode: 'US',
    language: 'en',
  });

  const updateFilter = (key, value) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const setMaxAgeDays = (days) => updateFilter('maxAgeDays', days);
  const setMaxVideos = (count) => updateFilter('maxVideos', count);
  const setMaxResults = (count) => updateFilter('maxResults', count);
  const setRegionCode = (code) => updateFilter('regionCode', code);
  const setLanguage = (lang) => updateFilter('language', lang);

  const resetFilters = () => {
    setFilters({
      maxAgeDays: 180,
      maxVideos: 15,
      minSubscribers: 1000,
      minTotalViews: 50000,
      maxResults: 50,
      regionCode: 'US',
      language: 'en',
    });
  };

  return {
    filters,
    setMaxAgeDays,
    setMaxVideos,
    setMaxResults,
    setRegionCode,
    setLanguage,
    updateFilter,
    resetFilters,
  };
};

export default useFilters;
