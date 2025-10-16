#!/usr/bin/env python3
"""
Content Cache - Save and load page content including HTML, CSS, and metadata

This module provides comprehensive caching of:
- Static HTML
- Rendered HTML (after JavaScript execution)
- CSS files (external and inline)
- HTTP headers
- Performance metrics
- Core Web Vitals
- BeautifulSoup objects (reconstructed from HTML)
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import json
import hashlib
import gzip
import base64
from urllib.parse import urlparse
import re

from src.core.content_fetcher import PageContent
from bs4 import BeautifulSoup


class ContentCache:
    """
    Manages comprehensive page content caching.
    
    Directory structure:
    cache_dir/
      └── {site_hash}/
          └── {url_hash}/
              ├── metadata.json      (URL, timestamps, metrics)
              ├── static.html.gz     (Static HTML, compressed)
              ├── rendered.html.gz   (Rendered HTML, compressed)
              ├── css/               (External CSS files)
              │   ├── main.css
              │   └── style.css
              └── resources/         (Other resources if needed)
    """
    
    def __init__(self, cache_dir: str = "output/content_cache"):
        """
        Initialize content cache.
        
        Args:
            cache_dir: Base directory for cache storage
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_url_hash(self, url: str) -> str:
        """
        Generate a unique hash for a URL.
        
        Args:
            url: URL to hash
            
        Returns:
            Short hash string (12 chars)
        """
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def _get_site_hash(self, root_url: str) -> str:
        """
        Generate a hash for the root domain.
        
        Args:
            root_url: Root URL
            
        Returns:
            Domain-based identifier
        """
        parsed = urlparse(root_url)
        domain = parsed.netloc.replace('www.', '')
        # Use domain name + hash for readability
        domain_clean = re.sub(r'[^a-zA-Z0-9]', '_', domain)
        return f"{domain_clean}_{hashlib.md5(domain.encode()).hexdigest()[:6]}"
    
    def _get_cache_path(self, root_url: str, url: str) -> Path:
        """
        Get the cache directory path for a specific URL.
        
        Args:
            root_url: Root URL of the crawl
            url: Specific URL being cached
            
        Returns:
            Path to cache directory
        """
        site_hash = self._get_site_hash(root_url)
        url_hash = self._get_url_hash(url)
        return self.cache_dir / site_hash / url_hash
    
    def save_content(
        self,
        root_url: str,
        content: PageContent,
        save_css: bool = True
    ) -> str:
        """
        Save page content to cache.
        
        Args:
            root_url: Root URL of the crawl
            content: PageContent object to cache
            save_css: Whether to extract and save CSS files
            
        Returns:
            Path to cached content directory
        """
        cache_path = self._get_cache_path(root_url, content.url)
        cache_path.mkdir(parents=True, exist_ok=True)
        
        # 1. Save metadata
        metadata = {
            'url': content.url,
            'cached_at': datetime.now().isoformat(),
            'status_code': content.status_code,
            'static_headers': content.static_headers,
            'static_load_time': content.static_load_time,
            'rendered_load_time': content.rendered_load_time,
            'performance_metrics': content.performance_metrics,
            'core_web_vitals': content.core_web_vitals,
            'has_static_html': bool(content.static_html),
            'has_rendered_html': bool(content.rendered_html),
            'static_size': len(content.static_html) if content.static_html else 0,
            'rendered_size': len(content.rendered_html) if content.rendered_html else 0
        }
        
        with open(cache_path / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        # 2. Save static HTML (compressed)
        if content.static_html:
            static_compressed = gzip.compress(content.static_html.encode('utf-8'))
            with open(cache_path / 'static.html.gz', 'wb') as f:
                f.write(static_compressed)
        
        # 3. Save rendered HTML (compressed)
        if content.rendered_html:
            rendered_compressed = gzip.compress(content.rendered_html.encode('utf-8'))
            with open(cache_path / 'rendered.html.gz', 'wb') as f:
                f.write(rendered_compressed)
        
        # 4. Extract and save CSS files
        if save_css and content.static_soup:
            css_dir = cache_path / 'css'
            css_dir.mkdir(exist_ok=True)
            
            css_files = self._extract_css(content)
            
            # Save inline styles
            inline_css = []
            for style_tag in content.static_soup.find_all('style'):
                if style_tag.string:
                    inline_css.append(style_tag.string)
            
            if inline_css:
                with open(css_dir / 'inline.css', 'w', encoding='utf-8') as f:
                    f.write('\n\n/* ===== INLINE STYLE BLOCK ===== */\n\n'.join(inline_css))
            
            # Save external CSS URLs (for future fetching)
            external_css = []
            for link in content.static_soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    external_css.append(href)
            
            if external_css:
                with open(css_dir / 'external_urls.json', 'w', encoding='utf-8') as f:
                    json.dump(external_css, f, indent=2)
        
        return str(cache_path)
    
    def _extract_css(self, content: PageContent) -> Dict[str, str]:
        """
        Extract CSS content from page.
        
        Args:
            content: PageContent object
            
        Returns:
            Dictionary of CSS filename -> content
        """
        css_files = {}
        
        # Get inline styles
        if content.static_soup:
            for i, style_tag in enumerate(content.static_soup.find_all('style')):
                if style_tag.string:
                    css_files[f'inline_{i}.css'] = style_tag.string
        
        return css_files
    
    def load_content(
        self,
        root_url: str,
        url: str,
        max_age_hours: Optional[int] = None
    ) -> Optional[PageContent]:
        """
        Load cached page content.
        
        Args:
            root_url: Root URL of the crawl
            url: Specific URL to load
            max_age_hours: Maximum cache age in hours (None = any age)
            
        Returns:
            PageContent object reconstructed from cache, or None if not found
        """
        cache_path = self._get_cache_path(root_url, url)
        
        if not cache_path.exists():
            return None
        
        # Load metadata
        metadata_file = cache_path / 'metadata.json'
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Check age
        if max_age_hours is not None:
            cached_at = datetime.fromisoformat(metadata['cached_at'])
            age_hours = (datetime.now() - cached_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                return None
        
        # Load HTML files
        static_html = None
        rendered_html = None
        
        static_file = cache_path / 'static.html.gz'
        if static_file.exists():
            with open(static_file, 'rb') as f:
                static_html = gzip.decompress(f.read()).decode('utf-8')
        
        rendered_file = cache_path / 'rendered.html.gz'
        if rendered_file.exists():
            with open(rendered_file, 'rb') as f:
                rendered_html = gzip.decompress(f.read()).decode('utf-8')
        
        # Create BeautifulSoup objects
        static_soup = BeautifulSoup(static_html, 'html.parser') if static_html else None
        rendered_soup = BeautifulSoup(rendered_html, 'html.parser') if rendered_html else None
        
        # Reconstruct PageContent object
        content = PageContent(
            url=metadata['url'],
            status_code=metadata['status_code'],
            static_html=static_html or '',
            static_soup=static_soup,
            static_headers=metadata.get('static_headers', {}),
            static_load_time=metadata.get('static_load_time', 0),
            rendered_html=rendered_html,
            rendered_soup=rendered_soup,
            rendered_load_time=metadata.get('rendered_load_time'),
            performance_metrics=metadata.get('performance_metrics', {}),
            core_web_vitals=metadata.get('core_web_vitals', {}),
            error=None
        )
        
        return content
    
    def get_cached_urls(self, root_url: str) -> List[str]:
        """
        Get list of all cached URLs for a site.
        
        Args:
            root_url: Root URL of the crawl
            
        Returns:
            List of cached URLs
        """
        site_hash = self._get_site_hash(root_url)
        site_cache = self.cache_dir / site_hash
        
        if not site_cache.exists():
            return []
        
        urls = []
        
        for url_dir in site_cache.iterdir():
            if url_dir.is_dir():
                metadata_file = url_dir / 'metadata.json'
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        urls.append(metadata['url'])
        
        return sorted(urls)
    
    def get_cache_stats(self, root_url: str) -> Dict[str, Any]:
        """
        Get statistics about cached content.
        
        Args:
            root_url: Root URL of the crawl
            
        Returns:
            Dictionary with cache statistics
        """
        site_hash = self._get_site_hash(root_url)
        site_cache = self.cache_dir / site_hash
        
        if not site_cache.exists():
            return {'total_urls': 0, 'total_size': 0}
        
        stats = {
            'total_urls': 0,
            'total_size': 0,
            'with_rendered': 0,
            'with_css': 0,
            'oldest_cache': None,
            'newest_cache': None
        }
        
        cache_times = []
        
        for url_dir in site_cache.iterdir():
            if url_dir.is_dir():
                metadata_file = url_dir / 'metadata.json'
                if metadata_file.exists():
                    stats['total_urls'] += 1
                    
                    # Get size
                    for file in url_dir.rglob('*'):
                        if file.is_file():
                            stats['total_size'] += file.stat().st_size
                    
                    # Load metadata
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        
                        if metadata.get('has_rendered_html'):
                            stats['with_rendered'] += 1
                        
                        if (url_dir / 'css').exists():
                            stats['with_css'] += 1
                        
                        cache_times.append(metadata['cached_at'])
        
        if cache_times:
            cache_times.sort()
            stats['oldest_cache'] = cache_times[0]
            stats['newest_cache'] = cache_times[-1]
        
        # Convert size to MB
        stats['total_size_mb'] = stats['total_size'] / (1024 * 1024)
        
        return stats
    
    def clear_cache(self, root_url: str):
        """
        Clear cached content for a site.
        
        Args:
            root_url: Root URL to clear cache for
        """
        site_hash = self._get_site_hash(root_url)
        site_cache = self.cache_dir / site_hash
        
        if site_cache.exists():
            import shutil
            shutil.rmtree(site_cache)
            print(f"Cleared cache for {root_url}")


def save_crawl_with_content(
    root_url: str,
    contents: List[PageContent],
    save_css: bool = True
) -> Dict[str, Any]:
    """
    Save entire crawl with all content.
    
    Args:
        root_url: Root URL of the crawl
        contents: List of PageContent objects
        save_css: Whether to save CSS files
        
    Returns:
        Summary of saved content
    """
    cache = ContentCache()
    
    saved = 0
    failed = 0
    total_size = 0
    
    print(f'\nCaching {len(contents)} pages...')
    
    for i, content in enumerate(contents, 1):
        try:
            cache_path = cache.save_content(root_url, content, save_css=save_css)
            saved += 1
            
            # Get size
            for file in Path(cache_path).rglob('*'):
                if file.is_file():
                    total_size += file.stat().st_size
            
            if i % 10 == 0:
                print(f'  Cached {i}/{len(contents)} pages...')
                
        except Exception as e:
            print(f'  Error caching {content.url}: {e}')
            failed += 1
    
    summary = {
        'total': len(contents),
        'saved': saved,
        'failed': failed,
        'total_size_mb': total_size / (1024 * 1024)
    }
    
    print(f'\nCache Summary:')
    print(f'  Saved: {saved}/{len(contents)} pages')
    print(f'  Total size: {summary["total_size_mb"]:.2f} MB')
    
    return summary

