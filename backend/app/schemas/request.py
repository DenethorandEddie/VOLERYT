from pydantic import BaseModel, Field
from typing import Optional


class NicheSearchRequest(BaseModel):
    """Request schema for niche search"""

    niche: str = Field(
        ...,
        description="Niche keyword to search for",
        min_length=2,
        max_length=100,
        example="basketball highlights"
    )
    max_channel_age_days: int = Field(
        default=180,
        description="Maximum channel age in days from first upload",
        ge=1,
        le=365,
        example=180
    )
    max_videos_per_channel: int = Field(
        default=15,
        description="Maximum number of videos per channel",
        ge=1,
        le=100,
        example=15
    )
    max_results: int = Field(
        default=50,
        description="Maximum number of channels to analyze",
        ge=1,
        le=100,
        example=50
    )
    region_code: str = Field(
        default="US",
        description="Region code for search",
        min_length=2,
        max_length=2,
        example="US"
    )
    language: str = Field(
        default="en",
        description="Language code for search (English only supported)",
        min_length=2,
        max_length=2,
        example="en"
    )


class ChannelAnalysisRequest(BaseModel):
    """Request schema for individual channel analysis"""

    channel_id: str = Field(
        ...,
        description="YouTube channel ID",
        min_length=10,
        max_length=50,
        example="UCuAXFkgsw1L7xaCfnd5JJOw"
    )


class ExportRequest(BaseModel):
    """Request schema for exporting results"""

    format: str = Field(
        default="csv",
        description="Export format (csv or json)",
        pattern="^(csv|json)$",
        example="csv"
    )
