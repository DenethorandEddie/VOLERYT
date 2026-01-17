from collections import Counter
from typing import List, Dict, Any
import re


# Common stop words to filter out
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
    'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its',
    'our', 'their', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
    'him', 'her', 'us', 'them', 'what', 'which', 'who', 'when', 'where',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now',
    'video', 'channel', 'new', 'first', 'episode', 'part', 'full', 'watch'
}


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract meaningful keywords from text

    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return

    Returns:
        List of keywords sorted by frequency
    """
    if not text:
        return []

    # Convert to lowercase and split into words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())

    # Filter out stop words and numbers
    meaningful_words = [
        word for word in words
        if word not in STOP_WORDS and not word.isdigit()
    ]

    # Count word frequencies
    word_counts = Counter(meaningful_words)

    # Return most common keywords
    return [word for word, count in word_counts.most_common(max_keywords)]


def detect_niche_from_titles(video_titles: List[str]) -> str:
    """
    Detect niche from video titles

    Args:
        video_titles: List of video titles

    Returns:
        Detected niche as a string
    """
    # Combine all titles
    combined_text = ' '.join(video_titles)

    # Extract top keywords
    keywords = extract_keywords(combined_text, max_keywords=3)

    if not keywords:
        return "general"

    # Create niche from top 2 keywords
    if len(keywords) >= 2:
        return f"{keywords[0]} {keywords[1]}"
    else:
        return keywords[0]


def detect_niche_from_channel(channel_info: Dict[str, Any], video_titles: List[str] = None) -> Dict[str, Any]:
    """
    Detect niche from channel information

    Args:
        channel_info: Channel information dict
        video_titles: Optional list of video titles

    Returns:
        Dict with detected niche and keywords
    """
    # Sources for niche detection
    channel_title = channel_info.get('title', '')
    channel_description = channel_info.get('description', '')

    # Extract keywords from different sources
    title_keywords = extract_keywords(channel_title, max_keywords=3)
    desc_keywords = extract_keywords(channel_description, max_keywords=5)

    video_keywords = []
    if video_titles:
        video_text = ' '.join(video_titles)
        video_keywords = extract_keywords(video_text, max_keywords=5)

    # Combine all keywords with weights
    all_keywords = []
    all_keywords.extend(title_keywords * 3)  # Title keywords have higher weight
    all_keywords.extend(video_keywords * 2)  # Video keywords have medium weight
    all_keywords.extend(desc_keywords)       # Description keywords have lower weight

    # Count combined keywords
    keyword_counts = Counter(all_keywords)
    top_keywords = [word for word, count in keyword_counts.most_common(5)]

    # Create niche from top 2-3 keywords
    if len(top_keywords) >= 2:
        niche = f"{top_keywords[0]} {top_keywords[1]}"
    elif len(top_keywords) == 1:
        niche = top_keywords[0]
    else:
        niche = "general content"

    return {
        'detected_niche': niche,
        'keywords': top_keywords[:5],
        'confidence': 'high' if len(top_keywords) >= 3 else 'medium' if len(top_keywords) >= 1 else 'low'
    }


# Broad search terms to discover channels across all niches
DISCOVERY_SEARCH_TERMS = [
    # General content types
    "vlog", "tutorial", "guide", "tips", "review", "shorts", "how to",

    # Gaming
    "gaming", "gameplay", "walkthrough", "game review", "streaming",

    # Technology
    "tech", "gadget", "unboxing", "smartphone", "laptop", "coding",

    # Cooking & Food
    "cooking", "recipe", "baking", "food", "kitchen", "meal prep",

    # Fitness & Health
    "fitness", "workout", "yoga", "gym", "exercise", "health",

    # Education
    "education", "learning", "study", "science", "math", "history",

    # Entertainment
    "comedy", "funny", "prank", "reaction", "challenge", "music",

    # Lifestyle
    "lifestyle", "daily vlog", "routine", "productivity", "organization",

    # Business & Finance
    "business", "investing", "finance", "crypto", "stocks", "entrepreneur",

    # Art & Creative
    "art", "drawing", "painting", "design", "photography", "animation",

    # Travel
    "travel", "destination", "adventure", "exploring", "vacation",

    # DIY & Crafts
    "diy", "craft", "handmade", "project", "build", "make",

    # Beauty & Fashion
    "beauty", "makeup", "skincare", "fashion", "style", "outfit",

    # Automotive
    "car", "automotive", "motorcycle", "vehicle", "driving",

    # Sports
    "sports", "football", "basketball", "soccer", "tennis", "training",

    # Pets & Animals
    "pet", "dog", "cat", "animal", "wildlife", "aquarium",

    # Documentary & News
    "documentary", "news", "current events", "politics", "analysis"
]
