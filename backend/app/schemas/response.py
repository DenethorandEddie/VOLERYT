from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class VideoInfo(BaseModel):
    """Individual video information"""

    video_id: str
    title: str
    published_at: str
    view_count: int
    like_count: Optional[int] = 0
    comment_count: Optional[int] = 0


class ChannelAnalysis(BaseModel):
    """Analyzed channel data"""

    channel_id: str
    channel_name: str
    channel_url: str
    thumbnail_url: Optional[str] = None

    # Age metrics
    first_upload_date: str
    age_days: int
    age_description: str
    tier: str
    tier_color: str

    # Video metrics
    video_count: int
    total_views: int
    subscriber_count: int
    avg_views_per_video: float

    # Viral videos
    viral_videos: List[VideoInfo] = []
    has_viral_content: bool = False


class NicheAnalysisResult(BaseModel):
    """Analysis result for a niche"""

    is_good_niche: bool
    competition_level: str  # "ideal", "good", "competitive", "saturated"
    reasons: List[str]


class NicheSearchResponse(BaseModel):
    """Response schema for niche search"""

    niche: str
    total_channels_found: int
    niche_pool_size: int  # Total videos across all channels

    channels: List[ChannelAnalysis]
    analysis: NicheAnalysisResult

    # Quota info
    quota_used: int
    quota_remaining: Optional[int] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""

    status: str
    youtube_api_connected: bool
    quota_remaining: Optional[int] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema"""

    error: str
    detail: Optional[str] = None
    error_type: Optional[str] = None
