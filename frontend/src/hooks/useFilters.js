import { useState } from 'react';

/**
 * Custom hook for managing filter state
 */
export const useFilters = () => {
  const [filters, setFilters] = useState({
    maxAgeDays: 180,         // 6 months default
    maxVideos: 15,           // 15 videos default
    minSubscribers: 100,     // Min 100 subscribers (yeni kanallar için)
    minTotalViews: 5000,     // Min 5K total views (yeni kanallar için)
    targetChannels: 50,      // Daha fazla kanal bul
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
      minSubscribers: 100,
      minTotalViews: 5000,
      targetChannels: 50,
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
