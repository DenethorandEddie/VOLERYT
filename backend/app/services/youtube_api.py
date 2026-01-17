from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional, Any
from app.config import settings
from app.services.quota_manager import quota_manager
import logging

logger = logging.getLogger(__name__)


class YouTubeAPIClient:
    """
    YouTube Data API v3 client with quota management
    """

    def __init__(self):
        self.api_key = settings.youtube_api_key
        self.service = build('youtube', 'v3', developerKey=self.api_key)

    def search_channels(
        self,
        query: str,
        region_code: str = "US",
        language: str = "en",
        max_results: int = 50,
        order: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search for channels by keyword

        Args:
            query: Search query
            region_code: Region code (e.g., "US")
            language: Language code (e.g., "en")
            max_results: Maximum results to return
            order: Sort order (relevance, date, viewCount)

        Returns:
            List of channel data

        Raises:
            Exception: If API call fails or quota exceeded
        """
        cost = settings.search_cost

        if not quota_manager.check_quota(cost):
            raise Exception(f"Quota exceeded. Remaining: {quota_manager.get_remaining_quota()}")

        try:
            logger.info(f"Searching channels for query: {query}")

            request = self.service.search().list(
                part="snippet",
                q=query,
                type="channel",
                regionCode=region_code,
                relevanceLanguage=language,
                maxResults=min(max_results, 50),  # API max is 50 per request
                order=order
            )

            response = request.execute()
            quota_manager.increment(cost)

            channels = []
            for item in response.get('items', []):
                channels.append({
                    'channel_id': item['id']['channelId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet'].get('description', ''),
                    'thumbnail': item['snippet']['thumbnails'].get('default', {}).get('url', ''),
                    'published_at': item['snippet']['publishedAt']
                })

            logger.info(f"Found {len(channels)} channels")
            return channels

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise Exception(f"YouTube API error: {str(e)}")

    def get_channel_details(self, channel_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed information for channels

        Args:
            channel_ids: List of channel IDs (max 50)

        Returns:
            List of channel details

        Raises:
            Exception: If API call fails
        """
        cost = settings.channel_details_cost

        if not quota_manager.check_quota(cost):
            raise Exception(f"Quota exceeded. Remaining: {quota_manager.get_remaining_quota()}")

        try:
            # API allows max 50 IDs per request
            channel_ids = channel_ids[:50]
            logger.info(f"Getting details for {len(channel_ids)} channels")

            request = self.service.channels().list(
                part="snippet,contentDetails,statistics",
                id=",".join(channel_ids)
            )

            response = request.execute()
            quota_manager.increment(cost)

            channels = []
            for item in response.get('items', []):
                channels.append({
                    'channel_id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet'].get('description', ''),
                    'thumbnail': item['snippet']['thumbnails'].get('default', {}).get('url', ''),
                    'published_at': item['snippet']['publishedAt'],
                    'uploads_playlist_id': item['contentDetails']['relatedPlaylists']['uploads'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
                    'video_count': int(item['statistics'].get('videoCount', 0))
                })

            return channels

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise Exception(f"YouTube API error: {str(e)}")

    def get_first_upload_date(self, uploads_playlist_id: str) -> Optional[str]:
        """
        Get the date of the first video uploaded to a channel

        CRITICAL: This gets the FIRST UPLOAD DATE, not channel creation date

        Args:
            uploads_playlist_id: The uploads playlist ID from channel details

        Returns:
            ISO format date string of first upload, or None if no videos

        Raises:
            Exception: If API call fails
        """
        cost = settings.playlist_items_cost

        if not quota_manager.check_quota(cost):
            raise Exception(f"Quota exceeded. Remaining: {quota_manager.get_remaining_quota()}")

        try:
            logger.info(f"Getting first upload date for playlist: {uploads_playlist_id}")

            # Get all video IDs (we need to paginate to find the oldest)
            all_videos = []
            next_page_token = None

            # Limit to prevent excessive API calls
            max_pages = 10  # Max 500 videos (50 per page)
            page_count = 0

            while page_count < max_pages:
                request = self.service.playlistItems().list(
                    part="contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )

                response = request.execute()
                quota_manager.increment(cost)

                items = response.get('items', [])
                all_videos.extend(items)

                next_page_token = response.get('nextPageToken')
                page_count += 1

                if not next_page_token:
                    break

            if not all_videos:
                logger.warning("No videos found in playlist")
                return None

            # The oldest video is the last one in the list
            oldest_video_id = all_videos[-1]['contentDetails']['videoId']

            # Get video details to get publish date
            video_details = self.get_video_details([oldest_video_id])

            if video_details:
                first_upload_date = video_details[0]['published_at']
                logger.info(f"First upload date: {first_upload_date}")
                return first_upload_date

            return None

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise Exception(f"YouTube API error: {str(e)}")

    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed information for videos

        Args:
            video_ids: List of video IDs (max 50)

        Returns:
            List of video details

        Raises:
            Exception: If API call fails
        """
        cost = settings.video_details_cost

        if not quota_manager.check_quota(cost):
            raise Exception(f"Quota exceeded. Remaining: {quota_manager.get_remaining_quota()}")

        try:
            # API allows max 50 IDs per request
            video_ids = video_ids[:50]

            request = self.service.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids)
            )

            response = request.execute()
            quota_manager.increment(cost)

            videos = []
            for item in response.get('items', []):
                videos.append({
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'comment_count': int(item['statistics'].get('commentCount', 0))
                })

            return videos

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise Exception(f"YouTube API error: {str(e)}")

    def get_all_channel_videos(
        self,
        uploads_playlist_id: str,
        max_videos: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all videos from a channel's uploads playlist

        Args:
            uploads_playlist_id: The uploads playlist ID
            max_videos: Maximum number of videos to retrieve

        Returns:
            List of video data with details

        Raises:
            Exception: If API call fails
        """
        cost_per_page = settings.playlist_items_cost

        try:
            logger.info(f"Getting videos from playlist: {uploads_playlist_id}")

            video_ids = []
            next_page_token = None
            max_pages = (max_videos // 50) + 1

            for _ in range(max_pages):
                if not quota_manager.check_quota(cost_per_page):
                    logger.warning("Quota limit reached while fetching videos")
                    break

                request = self.service.playlistItems().list(
                    part="contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )

                response = request.execute()
                quota_manager.increment(cost_per_page)

                for item in response.get('items', []):
                    video_ids.append(item['contentDetails']['videoId'])

                next_page_token = response.get('nextPageToken')

                if not next_page_token or len(video_ids) >= max_videos:
                    break

            # Get video details in batches of 50
            all_videos = []
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i:i + 50]
                videos = self.get_video_details(batch)
                all_videos.extend(videos)

            logger.info(f"Retrieved {len(all_videos)} videos")
            return all_videos

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise Exception(f"YouTube API error: {str(e)}")

    def test_api_key(self) -> bool:
        """
        Test if API key is valid

        Returns:
            True if valid, False otherwise
        """
        try:
            # Simple test: get a known channel
            request = self.service.channels().list(
                part="snippet",
                id="UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers channel
            )
            response = request.execute()
            return len(response.get('items', [])) > 0

        except HttpError as e:
            logger.error(f"API key test failed: {e}")
            return False


# Global YouTube API client instance
youtube_client = YouTubeAPIClient()
