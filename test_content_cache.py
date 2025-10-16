#!/usr/bin/env python3
"""
Test Content Caching System
"""

import sys
sys.path.insert(0, 'src')

from src.core.content_cache import ContentCache
from src.core.content_fetcher import ContentFetcher

print('='*80)
print('  TESTING CONTENT CACHE')
print('='*80)

# Test URL
url = 'https://www.applydigital.com'

# Step 1: Fetch content
print('\n[1] Fetching content...')
fetcher = ContentFetcher(enable_javascript=True)
content = fetcher.fetch_complete(url)

print(f'   Static HTML: {len(content.static_html)} bytes')
print(f'   Rendered HTML: {len(content.rendered_html or "")} bytes')
print(f'   Status Code: {content.status_code}')

# Step 2: Save to cache
print('\n[2] Saving to cache...')
cache = ContentCache()
cache_path = cache.save_content(url, content, save_css=True)
print(f'   Cached to: {cache_path}')

# Step 3: Load from cache
print('\n[3] Loading from cache...')
cached_content = cache.load_content(url, url, max_age_hours=24)

if cached_content:
    print(f'   [SUCCESS] Loaded from cache')
    print(f'   Static HTML: {len(cached_content.static_html)} bytes')
    print(f'   Rendered HTML: {len(cached_content.rendered_html or "")} bytes')
    print(f'   Has soup objects: {cached_content.static_soup is not None}')
    
    # Verify content matches
    if content.static_html == cached_content.static_html:
        print(f'   [SUCCESS] Static HTML matches original')
    else:
        print(f'   [ERROR] Static HTML does not match')
        
else:
    print(f'   [ERROR] Failed to load from cache')

# Step 4: Get cache stats
print('\n[4] Cache statistics...')
stats = cache.get_cache_stats(url)
print(f'   Total URLs cached: {stats["total_urls"]}')
print(f'   Total size: {stats["total_size_mb"]:.2f} MB')
print(f'   With rendered HTML: {stats["with_rendered"]}')
print(f'   With CSS: {stats["with_css"]}')

print('\n' + '='*80)
print('  CONTENT CACHE TEST COMPLETE')
print('='*80 + '\n')

