from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    youtube_api_key: str
    cors_origins: str = "http://localhost:3000,http://localhost:3001"

    # API quota settings
    daily_quota_limit: int = 10000
    search_cost: int = 100
    channel_details_cost: int = 1
    playlist_items_cost: int = 1
    video_details_cost: int = 1

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
