from typing import Literal


TierType = Literal["S+", "Great", "Good", "Average", "Possible", "Too Old"]


def calculate_tier(age_days: int) -> TierType:
    """
    Calculate channel tier based on age in days (from first upload)

    Tier system:
    - S+: ≤7 days (1 week)
    - Great: ≤30 days (1 month)
    - Good: ≤60 days (2 months)
    - Average: ≤90 days (3 months)
    - Possible: ≤150 days (5 months)
    - Too Old: >150 days (6+ months)

    Args:
        age_days: Channel age in days from first upload

    Returns:
        Tier string
    """
    if age_days <= 7:
        return "S+"
    elif age_days <= 30:
        return "Great"
    elif age_days <= 60:
        return "Good"
    elif age_days <= 90:
        return "Average"
    elif age_days <= 150:
        return "Possible"
    else:
        return "Too Old"


def get_tier_color(tier: TierType) -> str:
    """
    Get color code for tier badge

    Args:
        tier: Tier string

    Returns:
        Hex color code
    """
    colors = {
        "S+": "#FFD700",      # Gold
        "Great": "#10B981",   # Green
        "Good": "#3B82F6",    # Blue
        "Average": "#F59E0B", # Orange
        "Possible": "#6B7280", # Gray
        "Too Old": "#EF4444"  # Red
    }
    return colors.get(tier, "#6B7280")


def get_tier_score(tier: TierType) -> int:
    """
    Get numerical score for tier (for sorting)

    Args:
        tier: Tier string

    Returns:
        Score (higher is better)
    """
    scores = {
        "S+": 6,
        "Great": 5,
        "Good": 4,
        "Average": 3,
        "Possible": 2,
        "Too Old": 1
    }
    return scores.get(tier, 0)
