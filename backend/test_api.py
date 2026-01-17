#!/usr/bin/env python3
"""
Simple test script to verify YouTube API key is working
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.youtube_api import youtube_client
from services.quota_manager import quota_manager


def test_api_key():
    """Test if YouTube API key is valid"""
    print("Testing YouTube API key...")
    print(f"API Key: {youtube_client.api_key[:10]}...")

    try:
        is_valid = youtube_client.test_api_key()
        if is_valid:
            print("✓ API key is VALID")
            return True
        else:
            print("✗ API key test failed")
            return False
    except Exception as e:
        print(f"✗ Error testing API key: {e}")
        return False


def test_search():
    """Test searching for channels"""
    print("\nTesting channel search...")

    try:
        results = youtube_client.search_channels(
            query="basketball highlights",
            max_results=5
        )

        print(f"✓ Found {len(results)} channels")
        for i, channel in enumerate(results[:3], 1):
            print(f"  {i}. {channel['title']}")

        return True
    except Exception as e:
        print(f"✗ Search failed: {e}")
        return False


def test_quota_manager():
    """Test quota manager"""
    print("\nTesting quota manager...")

    try:
        info = quota_manager.get_quota_info()
        print(f"✓ Daily limit: {info['daily_limit']}")
        print(f"✓ Quota used: {info['quota_used']}")
        print(f"✓ Quota remaining: {info['quota_remaining']}")
        return True
    except Exception as e:
        print(f"✗ Quota manager failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("YouTube Niche Analyzer - API Test")
    print("=" * 50)

    tests = [
        ("API Key Validation", test_api_key),
        ("Channel Search", test_search),
        ("Quota Manager", test_quota_manager),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result for _, result in results)
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 50)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
