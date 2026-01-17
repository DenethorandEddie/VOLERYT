import { useState } from 'react';
import { searchNiche } from '../services/api';

/**
 * Custom hook for niche search functionality
 */
export const useSearch = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const performSearch = async (niche, filters) => {
    setLoading(true);
    setError(null);

    try {
      const searchParams = {
        niche: niche,
        max_channel_age_days: filters.maxAgeDays,
        max_videos_per_channel: filters.maxVideos,
        max_results: filters.maxResults || 50,
        region_code: filters.regionCode || 'US',
        language: filters.language || 'en',
      };

      const data = await searchNiche(searchParams);
      setResults(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearResults = () => {
    setResults(null);
    setError(null);
  };

  return {
    results,
    loading,
    error,
    performSearch,
    clearResults,
  };
};

export default useSearch;
