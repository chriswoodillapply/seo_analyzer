#!/usr/bin/env python3
"""
Crawl Cache - Save and load crawl results to avoid re-crawling

This module provides functionality to:
1. Save crawl results (URLs + metadata) to JSON
2. Load previously crawled URLs for testing
3. Build CrawlContext from cached data
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json
import hashlib


class CrawlCache:
    """
    Manages crawl result caching to disk.
    """
    
    def __init__(self, cache_dir: str = "output/crawl_cache"):
        """
        Initialize crawl cache.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, root_url: str, max_urls: int, depth: int) -> str:
        """
        Generate a unique cache key for a crawl configuration.
        
        Args:
            root_url: Root URL that was crawled
            max_urls: Maximum URLs crawled
            depth: Crawl depth
            
        Returns:
            Cache key (hash of parameters)
        """
        key_string = f"{root_url}_{max_urls}_{depth}"
        return hashlib.md5(key_string.encode()).hexdigest()[:12]
    
    def save_crawl(
        self,
        root_url: str,
        urls: List[str],
        metadata: Optional[Dict[str, Any]] = None,
        max_urls: int = 0,
        depth: int = 0
    ) -> str:
        """
        Save crawl results to cache.
        
        Args:
            root_url: Root URL that was crawled
            urls: List of discovered URLs
            metadata: Optional metadata (link graph, page info, etc.)
            max_urls: Maximum URLs in this crawl
            depth: Crawl depth
            
        Returns:
            Path to cache file
        """
        cache_key = self._get_cache_key(root_url, max_urls, depth)
        
        # Create cache data structure
        cache_data = {
            'root_url': root_url,
            'crawled_at': datetime.now().isoformat(),
            'total_urls': len(urls),
            'max_urls': max_urls,
            'depth': depth,
            'urls': urls,
            'metadata': metadata or {}
        }
        
        # Save to file
        cache_file = self.cache_dir / f"crawl_{cache_key}.json"
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"Crawl cached: {cache_file}")
        print(f"  URLs: {len(urls)}")
        print(f"  Cache key: {cache_key}")
        
        return str(cache_file)
    
    def load_crawl(
        self,
        root_url: str,
        max_urls: int = 0,
        depth: int = 0,
        max_age_hours: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Load crawl results from cache.
        
        Args:
            root_url: Root URL to load cache for
            max_urls: Maximum URLs parameter
            depth: Depth parameter
            max_age_hours: Optional maximum age in hours (None = any age)
            
        Returns:
            Cached crawl data, or None if not found/expired
        """
        cache_key = self._get_cache_key(root_url, max_urls, depth)
        cache_file = self.cache_dir / f"crawl_{cache_key}.json"
        
        if not cache_file.exists():
            return None
        
        # Load cache
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # Check age if specified
        if max_age_hours is not None:
            crawled_at = datetime.fromisoformat(cache_data['crawled_at'])
            age_hours = (datetime.now() - crawled_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                print(f"Cache expired ({age_hours:.1f} hours old, max {max_age_hours})")
                return None
        
        print(f"Loaded cached crawl: {cache_file}")
        print(f"  URLs: {cache_data['total_urls']}")
        print(f"  Crawled: {cache_data['crawled_at']}")
        
        return cache_data
    
    def list_caches(self) -> List[Dict[str, Any]]:
        """
        List all cached crawls.
        
        Returns:
            List of cache metadata
        """
        caches = []
        
        for cache_file in self.cache_dir.glob("crawl_*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                caches.append({
                    'file': str(cache_file),
                    'root_url': data.get('root_url'),
                    'total_urls': data.get('total_urls'),
                    'crawled_at': data.get('crawled_at'),
                    'max_urls': data.get('max_urls'),
                    'depth': data.get('depth')
                })
            except Exception:
                continue
        
        # Sort by crawl time (newest first)
        caches.sort(key=lambda x: x['crawled_at'], reverse=True)
        
        return caches
    
    def clear_cache(self, root_url: Optional[str] = None):
        """
        Clear cache files.
        
        Args:
            root_url: Optional URL to clear cache for (None = clear all)
        """
        if root_url:
            # Clear specific URL caches
            pattern = f"crawl_*.json"
            cleared = 0
            
            for cache_file in self.cache_dir.glob(pattern):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if data.get('root_url') == root_url:
                        cache_file.unlink()
                        cleared += 1
                except Exception:
                    continue
            
            print(f"Cleared {cleared} cache file(s) for {root_url}")
        else:
            # Clear all caches
            cleared = 0
            for cache_file in self.cache_dir.glob("crawl_*.json"):
                cache_file.unlink()
                cleared += 1
            
            print(f"Cleared all {cleared} cache file(s)")


def save_crawl_to_simple_list(urls: List[str], output_file: str = "output/crawled_urls.txt"):
    """
    Save URLs to a simple text file (one URL per line).
    
    This is useful for manual inspection or piping to other tools.
    
    Args:
        urls: List of URLs
        output_file: Output file path
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for url in sorted(urls):
            f.write(url + '\n')
    
    print(f"Saved {len(urls)} URLs to {output_file}")
    return str(output_path)


def load_urls_from_file(input_file: str) -> List[str]:
    """
    Load URLs from a text file (one per line).
    
    Args:
        input_file: Input file path
        
    Returns:
        List of URLs
    """
    urls = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith('#'):  # Skip comments
                urls.append(url)
    
    print(f"Loaded {len(urls)} URLs from {input_file}")
    return urls

