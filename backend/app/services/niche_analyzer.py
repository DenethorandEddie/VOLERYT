from typing import List, Dict, Any, Tuple
import statistics
import logging
from app.services.youtube_api import youtube_client
from app.utils.date_utils import calculate_days_since, format_date_for_display, get_age_description
from app.utils.tier_calculator import calculate_tier, get_tier_color, get_tier_score
from app.schemas.response import ChannelAnalysis, VideoInfo, NicheAnalysisResult

logger = logging.getLogger(__name__)


class NicheAnalyzer:
    """
    Core niche analysis algorithm
    Analyzes YouTube niches based on channel age, video count, and competition
    """

    def __init__(self):
        self.youtube = youtube_client

    def analyze_niche(
        self,
        niche_keyword: str,
        max_channel_age_days: int = 180,
        max_videos_per_channel: int = 15,
        max_results: int = 50,
        region_code: str = "US",
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Main niche analysis algorithm

        Steps:
        1. Search for channels matching niche keyword
        2. Filter by language (English only)
        3. Get channel details
        4. For each channel:
           - Get first upload date (CRITICAL: not channel creation)
           - Calculate age in days
           - Filter by age (<6 months)
           - Get video count
           - Filter by video count (≤15)
           - Assign tier
           - Get viral videos
        5. Calculate niche pool size
        6. Determine if good niche
        7. Sort by tier

        Args:
            niche_keyword: Niche to search for
            max_channel_age_days: Maximum channel age (default 180)
            max_videos_per_channel: Maximum videos per channel (default 15)
            max_results: Maximum channels to analyze (default 50)
            region_code: Region code for search
            language: Language code for search

        Returns:
            Dictionary with analyzed channels and niche metrics
        """
        logger.info(f"Starting niche analysis for: {niche_keyword}")

        # Step 1: Search for channels
        search_results = self.youtube.search_channels(
            query=niche_keyword,
            region_code=region_code,
            language=language,
            max_results=max_results
        )

        if not search_results:
            logger.info("No channels found for search query")
            return self._empty_result(niche_keyword)

        # Step 2: Get channel details
        channel_ids = [ch['channel_id'] for ch in search_results]
        channel_details = self.youtube.get_channel_details(channel_ids)

        logger.info(f"Analyzing {len(channel_details)} channels")

        # Step 3-4: Analyze each channel
        analyzed_channels = []
        for channel in channel_details:
            try:
                analysis = self._analyze_channel(
                    channel,
                    max_channel_age_days,
                    max_videos_per_channel
                )

                if analysis:
                    analyzed_channels.append(analysis)

            except Exception as e:
                logger.warning(f"Failed to analyze channel {channel['channel_id']}: {e}")
                continue

        logger.info(f"Successfully analyzed {len(analyzed_channels)} channels")

        # Step 5: Calculate niche pool size
        niche_pool_size = sum(ch.video_count for ch in analyzed_channels)

        # Step 6: Determine if good niche
        niche_analysis = self._analyze_niche_quality(
            len(analyzed_channels),
            niche_pool_size
        )

        # Step 7: Sort by tier (S+ first, then Great, etc.)
        analyzed_channels.sort(
            key=lambda x: get_tier_score(x.tier),
            reverse=True
        )

        return {
            'niche': niche_keyword,
            'total_channels_found': len(analyzed_channels),
            'niche_pool_size': niche_pool_size,
            'channels': analyzed_channels,
            'analysis': niche_analysis
        }

    def _analyze_channel(
        self,
        channel: Dict[str, Any],
        max_age_days: int,
        max_videos: int
    ) -> ChannelAnalysis | None:
        """
        Analyze a single channel

        Args:
            channel: Channel details from YouTube API
            max_age_days: Maximum allowed age in days
            max_videos: Maximum allowed video count

        Returns:
            ChannelAnalysis object if channel passes filters, None otherwise
        """
        channel_id = channel['channel_id']
        uploads_playlist_id = channel['uploads_playlist_id']

        # Get first upload date (CRITICAL)
        first_upload_date = self.youtube.get_first_upload_date(uploads_playlist_id)

        if not first_upload_date:
            logger.warning(f"Channel {channel_id} has no videos, skipping")
            return None

        # Calculate channel age from first upload
        age_days = calculate_days_since(first_upload_date)

        # Filter by age
        if age_days > max_age_days:
            logger.debug(f"Channel {channel_id} too old: {age_days} days")
            return None

        # Get video count
        video_count = channel['video_count']

        # Filter by video count
        if video_count > max_videos:
            logger.debug(f"Channel {channel_id} has too many videos: {video_count}")
            return None

        # Calculate tier
        tier = calculate_tier(age_days)

        # Get viral videos (only if channel has videos)
        viral_videos = []
        has_viral = False

        if video_count > 0 and video_count <= 50:  # Only analyze if reasonable number
            try:
                viral_videos = self._identify_viral_videos(
                    uploads_playlist_id,
                    max_videos=min(video_count, 50)
                )
                has_viral = len(viral_videos) > 0
            except Exception as e:
                logger.warning(f"Failed to get viral videos for {channel_id}: {e}")

        # Calculate average views
        avg_views = (
            channel['view_count'] / video_count if video_count > 0 else 0
        )

        # Build channel analysis
        return ChannelAnalysis(
            channel_id=channel_id,
            channel_name=channel['title'],
            channel_url=f"https://www.youtube.com/channel/{channel_id}",
            thumbnail_url=channel['thumbnail'],
            first_upload_date=format_date_for_display(first_upload_date),
            age_days=age_days,
            age_description=get_age_description(age_days),
            tier=tier,
            tier_color=get_tier_color(tier),
            video_count=video_count,
            total_views=channel['view_count'],
            subscriber_count=channel['subscriber_count'],
            avg_views_per_video=round(avg_views, 2),
            viral_videos=viral_videos[:5],  # Top 5 viral videos
            has_viral_content=has_viral
        )

    def _identify_viral_videos(
        self,
        uploads_playlist_id: str,
        max_videos: int = 50
    ) -> List[VideoInfo]:
        """
        Identify viral videos using statistical outlier detection

        A video is considered "viral" if its views are significantly above average:
        - Views > (mean + 2 * standard_deviation)
        - AND Views > (mean * 2)

        Args:
            uploads_playlist_id: Channel's uploads playlist ID
            max_videos: Maximum videos to analyze

        Returns:
            List of viral videos sorted by view count
        """
        try:
            videos = self.youtube.get_all_channel_videos(
                uploads_playlist_id,
                max_videos=max_videos
            )

            if len(videos) < 2:
                return []

            # Calculate statistics
            view_counts = [v['view_count'] for v in videos]
            mean_views = statistics.mean(view_counts)

            # Need at least 2 videos for stdev
            if len(view_counts) < 2:
                return []

            stdev_views = statistics.stdev(view_counts)

            # Viral threshold: mean + 2*stdev
            viral_threshold = mean_views + (2 * stdev_views)

            # Find viral videos
            viral_videos = []
            for video in videos:
                if (video['view_count'] > viral_threshold and
                    video['view_count'] > mean_views * 2):
                    viral_videos.append(VideoInfo(
                        video_id=video['video_id'],
                        title=video['title'],
                        published_at=format_date_for_display(video['published_at']),
                        view_count=video['view_count'],
                        like_count=video.get('like_count', 0),
                        comment_count=video.get('comment_count', 0)
                    ))

            # Sort by views (highest first)
            viral_videos.sort(key=lambda x: x.view_count, reverse=True)

            return viral_videos

        except Exception as e:
            logger.warning(f"Error identifying viral videos: {e}")
            return []

    def _analyze_niche_quality(
        self,
        channel_count: int,
        video_pool_size: int
    ) -> NicheAnalysisResult:
        """
        Determine if niche meets "good niche" criteria

        Criteria:
        - Ideal: ≤5 channels AND ≤50 videos
        - Good: ≤10 channels AND ≤100 videos
        - Competitive: ≤20 channels AND ≤200 videos
        - Saturated: >20 channels OR >200 videos

        Args:
            channel_count: Number of channels in niche
            video_pool_size: Total videos in niche pool

        Returns:
            NicheAnalysisResult with quality assessment
        """
        reasons = []

        # Determine competition level
        if channel_count <= 5 and video_pool_size <= 50:
            competition_level = "ideal"
            is_good = True
            reasons.append("✓ Ideal niche: Very low competition")
            reasons.append(f"✓ Only {channel_count} channels (target: ≤5)")
            reasons.append(f"✓ Only {video_pool_size} videos in pool (target: ≤50)")

        elif channel_count <= 10 and video_pool_size <= 100:
            competition_level = "good"
            is_good = True
            reasons.append("✓ Good niche: Low competition")
            reasons.append(f"✓ {channel_count} channels (target: ≤10)")
            reasons.append(f"✓ {video_pool_size} videos in pool (target: ≤100)")

        elif channel_count <= 20 and video_pool_size <= 200:
            competition_level = "competitive"
            is_good = False
            reasons.append("⚠ Competitive niche: Moderate competition")
            reasons.append(f"⚠ {channel_count} channels (better if ≤10)")
            reasons.append(f"⚠ {video_pool_size} videos in pool (better if ≤100)")

        else:
            competition_level = "saturated"
            is_good = False
            reasons.append("✗ Saturated niche: High competition")
            reasons.append(f"✗ {channel_count} channels (too many, target: ≤10)")
            reasons.append(f"✗ {video_pool_size} videos in pool (too many, target: ≤100)")

        return NicheAnalysisResult(
            is_good_niche=is_good,
            competition_level=competition_level,
            reasons=reasons
        )

    def _empty_result(self, niche_keyword: str) -> Dict[str, Any]:
        """Return empty result when no channels found"""
        return {
            'niche': niche_keyword,
            'total_channels_found': 0,
            'niche_pool_size': 0,
            'channels': [],
            'analysis': NicheAnalysisResult(
                is_good_niche=False,
                competition_level="unknown",
                reasons=["No channels found matching criteria"]
            )
        }


# Global niche analyzer instance
niche_analyzer = NicheAnalyzer()
