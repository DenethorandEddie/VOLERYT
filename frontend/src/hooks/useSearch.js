import { useState } from 'react';
import { searchNiche, discoverChannels } from '../services/api';

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

  const performDiscover = async (filters) => {
    setLoading(true);
    setError(null);

    try {
      const data = await discoverChannels(filters);

      // Transform discovered channels to match results format
      const transformedData = {
        niche: 'All Niches (Discovery Mode)',
        total_channels_found: data.total_channels,
        niche_pool_size: data.discovered_channels.reduce((sum, ch) => sum + ch.video_count, 0),
        channels: data.discovered_channels.map(ch => ({
          channel_id: ch.channel_id,
          channel_name: ch.channel_name,
          channel_url: ch.channel_url,
          thumbnail_url: ch.thumbnail_url,
          first_upload_date: ch.first_upload_date,
          age_days: ch.age_days,
          age_description: ch.age_description,
          tier: ch.tier,
          tier_color: ch.tier_color,
          video_count: ch.video_count,
          total_views: ch.total_views,
          subscriber_count: ch.subscriber_count,
          avg_views_per_video: ch.avg_views_per_video,
          viral_videos: [],
          has_viral_content: false,
          detected_niche: ch.detected_niche, // Extra field for discovery
          keywords: ch.keywords, // Extra field for discovery
        })),
        analysis: {
          is_good_niche: true,
          competition_level: 'discovery',
          reasons: [
            `✓ Discovered ${data.total_channels} channels across ${data.total_niches} different niches`,
            `✓ Niches found: ${data.niches.slice(0, 5).join(', ')}${data.niches.length > 5 ? '...' : ''}`
          ]
        },
        quota_used: data.quota_used,
        quota_remaining: data.quota_remaining,
        discovery_mode: true,
        niches_found: data.niches,
        grouped_by_niche: data.grouped_by_niche
      };

      setResults(transformedData);
      return transformedData;
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
    performDiscover,
    clearResults,
  };
};

export default useSearch;
