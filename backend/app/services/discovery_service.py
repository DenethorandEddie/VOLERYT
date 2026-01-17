from typing import List, Dict, Any
import logging
import random
from app.services.youtube_api import youtube_client
from app.utils.date_utils import calculate_days_since, format_date_for_display, get_age_description
from app.utils.tier_calculator import calculate_tier, get_tier_color
from app.utils.niche_detector import detect_niche_from_channel, DISCOVERY_SEARCH_TERMS

logger = logging.getLogger(__name__)


class DiscoveryService:
    """
    Service for discovering channels across all YouTube niches
    """

    def __init__(self):
        self.youtube = youtube_client

    def discover_channels(
        self,
        max_channel_age_days: int = 180,
        max_videos_per_channel: int = 15,
        min_subscribers: int = 1000,
        min_total_views: int = 50000,
        target_channels: int = 20,
        search_terms_limit: int = 15
    ) -> Dict[str, Any]:
        """
        Discover channels across all YouTube niches

        Strategy:
        1. Use broad search terms to find channels
        2. Order by date to get newest content
        3. Analyze each channel and detect its niche
        4. Filter by age, video count, subscribers, and views
        5. Return diverse set of channels from different niches

        Args:
            max_channel_age_days: Maximum channel age from first upload
            max_videos_per_channel: Maximum videos per channel
            min_subscribers: Minimum subscriber count
            min_total_views: Minimum total view count
            target_channels: Target number of channels to find
            search_terms_limit: Number of search terms to use

        Returns:
            Dict with discovered channels and niche groupings
        """
        logger.info(f"Starting YouTube-wide discovery (target: {target_channels} channels)")

        # Select random search terms for diversity
        search_terms = random.sample(
            DISCOVERY_SEARCH_TERMS,
            min(search_terms_limit, len(DISCOVERY_SEARCH_TERMS))
        )

        discovered_channels = []
        channels_per_term = max(3, target_channels // len(search_terms))

        for term in search_terms:
            if len(discovered_channels) >= target_channels:
                break

            try:
                logger.info(f"🔍 Searching: '{term}'")

                # Search by date to get newest content
                results = self.youtube.search_channels(
                    query=term,
                    max_results=10,
                    order="date"  # Get newest channels/content
                )

                if not results:
                    continue

                # Get channel details
                channel_ids = [ch['channel_id'] for ch in results]
                channel_details = self.youtube.get_channel_details(channel_ids)

                # Analyze each channel
                for channel in channel_details[:channels_per_term]:
                    try:
                        analyzed = self._analyze_discovered_channel(
                            channel,
                            max_channel_age_days,
                            max_videos_per_channel,
                            min_subscribers,
                            min_total_views
                        )

                        if analyzed:
                            discovered_channels.append(analyzed)
                            logger.info(
                                f"✅ Found: {analyzed['channel_name']} "
                                f"[{analyzed['detected_niche']}] - "
                                f"Tier: {analyzed['tier']}, Videos: {analyzed['video_count']}"
                            )

                    except Exception as e:
                        logger.warning(f"Failed to analyze channel: {e}")
                        continue

            except Exception as e:
                logger.warning(f"Search failed for '{term}': {e}")
                continue

        # Group by detected niche
        niche_groups = {}
        for channel in discovered_channels:
            niche = channel['detected_niche']
            if niche not in niche_groups:
                niche_groups[niche] = []
            niche_groups[niche].append(channel)

        # Sort channels by tier score
        discovered_channels.sort(
            key=lambda x: self._get_tier_score(x['tier']),
            reverse=True
        )

        logger.info(
            f"Discovery complete: {len(discovered_channels)} channels found "
            f"across {len(niche_groups)} niches"
        )

        return {
            'discovered_channels': discovered_channels,
            'total_channels': len(discovered_channels),
            'total_niches': len(niche_groups),
            'niches': list(niche_groups.keys()),
            'grouped_by_niche': {
                niche: len(channels)
                for niche, channels in niche_groups.items()
            }
        }

    def _analyze_discovered_channel(
        self,
        channel: Dict[str, Any],
        max_age_days: int,
        max_videos: int,
        min_subscribers: int,
        min_total_views: int
    ) -> Dict[str, Any] | None:
        """
        Analyze a discovered channel

        Args:
            channel: Channel details from YouTube API
            max_age_days: Maximum allowed age
            max_videos: Maximum allowed video count
            min_subscribers: Minimum subscriber count
            min_total_views: Minimum total view count

        Returns:
            Analyzed channel dict or None if filtered out
        """
        channel_id = channel['channel_id']
        uploads_playlist_id = channel['uploads_playlist_id']

        # Get first upload date
        first_upload_date = self.youtube.get_first_upload_date(uploads_playlist_id)

        if not first_upload_date:
            return None

        # Calculate age
        age_days = calculate_days_since(first_upload_date)

        # Filter by age
        if age_days > max_age_days:
            logger.debug(f"Filtered: {channel['title']} - too old ({age_days} days)")
            return None

        # Filter by video count
        video_count = channel['video_count']
        if video_count > max_videos:
            logger.debug(f"Filtered: {channel['title']} - too many videos ({video_count})")
            return None

        # Filter by subscriber count
        subscriber_count = channel['subscriber_count']
        if subscriber_count < min_subscribers:
            logger.debug(f"Filtered: {channel['title']} - too few subscribers ({subscriber_count})")
            return None

        # Filter by total views
        total_views = channel['view_count']
        if total_views < min_total_views:
            logger.debug(f"Filtered: {channel['title']} - too few views ({total_views})")
            return None

        # Get some video titles for niche detection
        video_titles = []
        try:
            videos = self.youtube.get_all_channel_videos(
                uploads_playlist_id,
                max_videos=min(10, video_count)
            )
            video_titles = [v['title'] for v in videos]
        except Exception as e:
            logger.warning(f"Failed to get video titles for niche detection: {e}")

        # Detect niche
        niche_info = detect_niche_from_channel(channel, video_titles)

        # Calculate tier
        tier = calculate_tier(age_days)

        # Build result
        return {
            'channel_id': channel_id,
            'channel_name': channel['title'],
            'channel_url': f"https://www.youtube.com/channel/{channel_id}",
            'thumbnail_url': channel.get('thumbnail', ''),
            'detected_niche': niche_info['detected_niche'],
            'keywords': niche_info['keywords'],
            'niche_confidence': niche_info['confidence'],
            'first_upload_date': format_date_for_display(first_upload_date),
            'age_days': age_days,
            'age_description': get_age_description(age_days),
            'tier': tier,
            'tier_color': get_tier_color(tier),
            'video_count': video_count,
            'subscriber_count': channel['subscriber_count'],
            'total_views': channel['view_count'],
            'avg_views_per_video': round(
                channel['view_count'] / video_count if video_count > 0 else 0,
                2
            )
        }

    def _get_tier_score(self, tier: str) -> int:
        """Get numerical score for tier sorting"""
        scores = {
            "S+": 6,
            "Great": 5,
            "Good": 4,
            "Average": 3,
            "Possible": 2,
            "Too Old": 1
        }
        return scores.get(tier, 0)


# Global discovery service instance
discovery_service = DiscoveryService()
