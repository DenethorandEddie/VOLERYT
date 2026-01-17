from fastapi import APIRouter, HTTPException, Query, status
from app.services.discovery_service import discovery_service
from app.services.quota_manager import quota_manager
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/discover", tags=["discover"])


@router.get("/channels")
async def discover_channels(
    max_channel_age_days: int = Query(
        default=180,
        ge=1,
        le=365,
        description="Maximum channel age in days from first upload"
    ),
    max_videos_per_channel: int = Query(
        default=15,
        ge=1,
        le=100,
        description="Maximum videos per channel"
    ),
    min_subscribers: int = Query(
        default=100,
        ge=0,
        le=1000000,
        description="Minimum subscriber count (100 for new channels)"
    ),
    min_total_views: int = Query(
        default=5000,
        ge=0,
        le=100000000,
        description="Minimum total view count (5K for new channels)"
    ),
    target_channels: int = Query(
        default=50,
        ge=5,
        le=100,
        description="Target number of channels to discover"
    )
):
    """
    Discover channels across all YouTube niches

    This endpoint:
    1. Searches YouTube with broad terms across all categories
    2. Finds newest channels ordered by date
    3. Automatically detects each channel's niche
    4. Filters by age and video count
    5. Returns diverse channels from different niches

    **Discovery Strategy:**
    - Uses 15+ different search categories
    - Orders by date to find newest content
    - Detects niche from channel titles, descriptions, and video titles
    - Groups results by detected niche

    **Filters:**
    - Channel age: from first upload (NOT channel creation)
    - Video count: maximum videos on channel
    - Minimum subscribers: filter out channels with too few subscribers
    - Minimum total views: filter out channels with too few total views
    - Only English channels

    **Returns:**
    - Discovered channels with auto-detected niches
    - Tier ratings (S+, Great, Good, etc.)
    - Niche groupings and statistics
    """
    try:
        logger.info(
            f"Starting discovery: max_age={max_channel_age_days}d, "
            f"max_videos={max_videos_per_channel}, min_subs={min_subscribers}, "
            f"min_views={min_total_views}, target={target_channels}"
        )

        # Check quota
        quota_info = quota_manager.get_quota_info()
        required_quota = target_channels * 15  # Rough estimate

        if quota_info['quota_remaining'] < required_quota:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Insufficient API quota. Need ~{required_quota}, have {quota_info['quota_remaining']}"
            )

        # Get quota before discovery
        quota_before = quota_manager.quota_used

        # Perform discovery
        result = discovery_service.discover_channels(
            max_channel_age_days=max_channel_age_days,
            max_videos_per_channel=max_videos_per_channel,
            min_subscribers=min_subscribers,
            min_total_views=min_total_views,
            target_channels=target_channels,
            search_terms_limit=30
        )

        # Calculate quota used
        quota_after = quota_manager.quota_used
        quota_used_for_discovery = quota_after - quota_before
        updated_quota = quota_manager.get_quota_info()

        # Add quota info to response
        result['quota_used'] = quota_used_for_discovery
        result['quota_remaining'] = updated_quota['quota_remaining']

        logger.info(
            f"Discovery completed: {result['total_channels']} channels "
            f"across {result['total_niches']} niches, "
            f"quota used: {quota_used_for_discovery}"
        )

        return result

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error during discovery: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error discovering channels: {str(e)}"
        )
