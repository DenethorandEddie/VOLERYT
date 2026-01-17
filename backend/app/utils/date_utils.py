from datetime import datetime, timezone
from typing import Optional


def parse_youtube_date(date_string: str) -> datetime:
    """
    Parse YouTube API date string to datetime object
    YouTube uses ISO 8601 format: 2025-01-17T12:00:00Z
    """
    try:
        # YouTube dates are in UTC with 'Z' suffix
        if date_string.endswith('Z'):
            date_string = date_string[:-1] + '+00:00'
        return datetime.fromisoformat(date_string)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid date format: {date_string}") from e


def calculate_days_since(date_string: str) -> int:
    """
    Calculate number of days between a date string and now

    Args:
        date_string: ISO format date string from YouTube API

    Returns:
        Number of days (integer)
    """
    upload_date = parse_youtube_date(date_string)
    now = datetime.now(timezone.utc)

    # Calculate difference in days
    delta = now - upload_date
    return delta.days


def format_date_for_display(date_string: str) -> str:
    """
    Format YouTube date for user-friendly display

    Args:
        date_string: ISO format date string

    Returns:
        Formatted date string (e.g., "2025-01-17")
    """
    try:
        date_obj = parse_youtube_date(date_string)
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return date_string


def get_age_description(days: int) -> str:
    """
    Get human-readable age description

    Args:
        days: Number of days

    Returns:
        Description like "1 week", "2 months", etc.
    """
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''}"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''}"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''}"
    else:
        years = days // 365
        return f"{years} year{'s' if years != 1 else ''}"
