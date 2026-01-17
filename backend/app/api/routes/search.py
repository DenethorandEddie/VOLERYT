from fastapi import APIRouter, HTTPException, status
from app.schemas.request import NicheSearchRequest, ChannelAnalysisRequest
from app.schemas.response import NicheSearchResponse, HealthCheckResponse, ErrorResponse
from app.services.niche_analyzer import niche_analyzer
from app.services.quota_manager import quota_manager
from app.services.youtube_api import youtube_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.post(
    "/search/niche",
    response_model=NicheSearchResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def search_niche(request: NicheSearchRequest):
    """
    Search and analyze a YouTube niche

    This endpoint:
    1. Searches for channels matching the niche keyword
    2. Filters channels by age (from first upload) and video count
    3. Assigns tier ratings (S+, Great, Good, etc.)
    4. Calculates niche pool size and competition metrics
    5. Returns sorted results with viral video analysis

    **Filters:**
    - Channel age: from first upload date (NOT channel creation)
    - Video count: total videos on channel
    - Language: English only
    - Region: US by default

    **Tiers:**
    - S+: ≤7 days old
    - Great: ≤30 days old
    - Good: ≤60 days old
    - Average: ≤90 days old
    - Possible: ≤150 days old
    """
    try:
        logger.info(f"Received niche search request: {request.niche}")

        # Check quota before processing
        quota_info = quota_manager.get_quota_info()
        if quota_info['quota_remaining'] < 200:  # Need at least 200 units for a search
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Insufficient API quota. Remaining: {quota_info['quota_remaining']} units"
            )

        # Perform analysis
        result = niche_analyzer.analyze_niche(
            niche_keyword=request.niche,
            max_channel_age_days=request.max_channel_age_days,
            max_videos_per_channel=request.max_videos_per_channel,
            max_results=request.max_results,
            region_code=request.region_code,
            language=request.language
        )

        # Get updated quota info
        updated_quota = quota_manager.get_quota_info()
        quota_used_for_search = quota_info['quota_used']
        final_quota_used = updated_quota['quota_used'] - quota_used_for_search

        # Build response
        response = NicheSearchResponse(
            niche=result['niche'],
            total_channels_found=result['total_channels_found'],
            niche_pool_size=result['niche_pool_size'],
            channels=result['channels'],
            analysis=result['analysis'],
            quota_used=final_quota_used,
            quota_remaining=updated_quota['quota_remaining']
        )

        logger.info(
            f"Search completed: {response.total_channels_found} channels, "
            f"{response.niche_pool_size} videos in pool, "
            f"quota used: {final_quota_used}"
        )

        return response

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error processing niche search: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing niche: {str(e)}"
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    responses={500: {"model": ErrorResponse}}
)
async def health_check():
    """
    Health check endpoint

    Verifies:
    - API is running
    - YouTube API connection is working
    - API key is valid
    - Quota status
    """
    try:
        # Test YouTube API connection
        api_connected = youtube_client.test_api_key()

        # Get quota info
        quota_info = quota_manager.get_quota_info()

        if not api_connected:
            return HealthCheckResponse(
                status="unhealthy",
                youtube_api_connected=False,
                message="YouTube API connection failed. Check API key."
            )

        return HealthCheckResponse(
            status="healthy",
            youtube_api_connected=True,
            quota_remaining=quota_info['quota_remaining'],
            message="All systems operational"
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            youtube_api_connected=False,
            message=f"Health check failed: {str(e)}"
        )


@router.get("/quota")
async def get_quota_info():
    """
    Get current API quota information

    Returns:
        Quota usage details including daily limit, used, and remaining
    """
    return quota_manager.get_quota_info()
