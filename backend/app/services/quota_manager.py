from datetime import datetime, timedelta
from typing import Optional
from app.config import settings


class QuotaManager:
    """
    Manages YouTube API quota usage
    Daily limit: 10,000 units
    """

    def __init__(self):
        self.daily_limit = settings.daily_quota_limit
        self.quota_used = 0
        self.reset_time: Optional[datetime] = None
        self._reset_quota_if_needed()

    def _reset_quota_if_needed(self):
        """Reset quota if we've passed midnight UTC"""
        now = datetime.utcnow()

        if self.reset_time is None or now >= self.reset_time:
            # Reset at midnight UTC
            self.quota_used = 0
            tomorrow = now + timedelta(days=1)
            self.reset_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day)

    def check_quota(self, cost: int) -> bool:
        """
        Check if we have enough quota for an operation

        Args:
            cost: Quota cost of the operation

        Returns:
            True if quota available, False otherwise
        """
        self._reset_quota_if_needed()
        return (self.quota_used + cost) <= self.daily_limit

    def increment(self, cost: int):
        """
        Increment quota usage

        Args:
            cost: Quota cost to add
        """
        self._reset_quota_if_needed()
        self.quota_used += cost

    def get_remaining_quota(self) -> int:
        """Get remaining quota for today"""
        self._reset_quota_if_needed()
        return max(0, self.daily_limit - self.quota_used)

    def get_quota_info(self) -> dict:
        """Get detailed quota information"""
        self._reset_quota_if_needed()
        return {
            "daily_limit": self.daily_limit,
            "quota_used": self.quota_used,
            "quota_remaining": self.get_remaining_quota(),
            "reset_time": self.reset_time.isoformat() if self.reset_time else None
        }


# Global quota manager instance
quota_manager = QuotaManager()
