#!/usr/bin/env python3
"""
URLCrawler - Discovers URLs from websites using static and JavaScript rendering
"""

from typing import List, Set, Dict, Optional
from urllib.parse import urlparse, urljoin
from collections import deque
import requests
from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class URLCrawler:
    """
    Enterprise URL crawler that discovers URLs using both
    static HTML parsing and JavaScript rendering
    """
    
    def __init__(
        self,
        max_depth: int = 3,
        max_urls: int = 1000,
        use_javascript: bool = True,
        timeout: int = 30,
        user_agent: Optional[str] = None
    ):
        """
        Initialize URL Crawler
        
        Args:
            max_depth: Maximum crawl depth
            max_urls: Maximum URLs to discover
            use_javascript: Enable JavaScript rendering
            timeout: Request timeout in seconds
            user_agent: Custom user agent string
        """
        self.max_depth = max_depth
        self.max_urls = max_urls
        self.use_javascript = use_javascript and PLAYWRIGHT_AVAILABLE
        self.timeout = timeout
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36'
        )
        
        # URL tracking
        self.discovered_urls: Dict[str, dict] = {}
        self.visited_urls: Set[str] = set()
        self.failed_urls: Dict[str, str] = {}
        
        # Setup session
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        # Playwright setup
        self.playwright = None
        self.browser = None
        self.context = None
        
        if self.use_javascript:
            self._setup_playwright()
    
    def _setup_playwright(self):
        """Initialize Playwright"""
        if not PLAYWRIGHT_AVAILABLE:
            return
        
        try:
            # Check if we're in an asyncio event loop
            import asyncio
            try:
                asyncio.get_running_loop()
                # We're in an event loop, need to handle differently
                print("Note: Running in async context, using alternative Playwright setup")
                # For now, disable JS rendering in crawler (ContentFetcher will still work)
                self.use_javascript = False
                return
            except RuntimeError:
                # No event loop running, safe to use sync API
                pass
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=self.user_agent
            )
        except Exception as e:
            print(f"Warning: Playwright initialization failed: {e}")
            self.use_javascript = False
    
    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL is valid and belongs to base domain"""
        try:
            parsed = urlparse(url)
            base_parsed = urlparse(base_domain)
            
            # Must be same domain
            if parsed.netloc != base_parsed.netloc:
                return False
            
            # Skip non-http(s) URLs
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Skip common file types
            excluded_extensions = [
                '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
                '.zip', '.tar', '.gz', '.mp4', '.mp3', '.avi', '.mov',
                '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.css', '.js', '.xml', '.json', '.txt'
            ]
            
            if any(url.lower().endswith(ext) for ext in excluded_extensions):
                return False
            
            return True
            
        except:
            return False
    
    def _clean_url(self, url: str) -> str:
        """Clean and normalize URL"""
        # Remove fragments
        if '#' in url:
            url = url.split('#')[0]
        
        # Remove trailing slash for consistency
        if url.endswith('/') and url.count('/') > 3:
            url = url.rstrip('/')
        
        return url
    
    def _get_urls_from_static_html(self, url: str) -> List[str]:
        """Extract URLs from static HTML"""
        urls = []
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if not href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                        full_url = urljoin(url, href)
                        urls.append(full_url)
        except Exception as e:
            self.failed_urls[url] = str(e)
        
        return urls
    
    def _get_urls_from_javascript(self, url: str) -> List[str]:
        """Extract URLs from JavaScript-rendered content"""
        urls = []
        
        if not self.use_javascript or not self.context:
            return urls
        
        try:
            page = self.context.new_page()
            page.goto(url, timeout=self.timeout * 1000, wait_until='networkidle')
            page.wait_for_timeout(2000)
            
            # Get all links
            links = page.query_selector_all('a[href]')
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and not href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                        full_url = urljoin(url, href)
                        urls.append(full_url)
                except:
                    continue
            
            page.close()
            
        except Exception as e:
            if url not in self.failed_urls:
                self.failed_urls[url] = f"JavaScript rendering: {str(e)}"
        
        return urls
    
    def crawl(self, start_urls: List[str]) -> List[str]:
        """
        Crawl websites starting from given URLs
        
        Args:
            start_urls: List of starting URLs
            
        Returns:
            List of discovered URLs
        """
        queue = deque()
        
        # Initialize queue with start URLs
        for url in start_urls:
            queue.append((url, 0, 'seed'))
            base_domain = urlparse(url).netloc
        
        while queue and len(self.discovered_urls) < self.max_urls:
            current_url, depth, source = queue.popleft()
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
            
            # Skip if max depth exceeded
            if depth > self.max_depth:
                continue
            
            self.visited_urls.add(current_url)
            
            # Add to discovered URLs
            if current_url not in self.discovered_urls:
                self.discovered_urls[current_url] = {
                    'depth': depth,
                    'source': source,
                    'discovery_method': []
                }
            
            # Discover new URLs
            new_urls = []
            
            # Static HTML discovery
            static_urls = self._get_urls_from_static_html(current_url)
            for url in static_urls:
                new_urls.append(('static', url))
            
            # JavaScript discovery
            if self.use_javascript and depth < self.max_depth:
                js_urls = self._get_urls_from_javascript(current_url)
                for url in js_urls:
                    new_urls.append(('javascript', url))
            
            # Process discovered URLs
            for method, url in new_urls:
                # Check if we've reached the max URLs limit
                if len(self.discovered_urls) >= self.max_urls:
                    break
                
                cleaned_url = self._clean_url(url)
                
                if not self._is_valid_url(cleaned_url, start_urls[0]):
                    continue
                
                if cleaned_url not in self.discovered_urls:
                    self.discovered_urls[cleaned_url] = {
                        'depth': depth + 1,
                        'source': current_url,
                        'discovery_method': [method]
                    }
                    
                    # Add to queue for further exploration
                    if depth + 1 <= self.max_depth:
                        queue.append((cleaned_url, depth + 1, current_url))
                else:
                    # Track discovery method
                    if method not in self.discovered_urls[cleaned_url]['discovery_method']:
                        self.discovered_urls[cleaned_url]['discovery_method'].append(method)
        
        return list(self.discovered_urls.keys())
    
    def get_urls_by_depth(self, depth: int) -> List[str]:
        """Get all URLs at a specific depth"""
        return [
            url for url, data in self.discovered_urls.items()
            if data['depth'] == depth
        ]
    
    def get_statistics(self) -> Dict:
        """Get crawl statistics"""
        depth_counts = {}
        for url_data in self.discovered_urls.values():
            depth = url_data['depth']
            depth_counts[depth] = depth_counts.get(depth, 0) + 1
        
        return {
            'total_urls': len(self.discovered_urls),
            'visited_urls': len(self.visited_urls),
            'failed_urls': len(self.failed_urls),
            'by_depth': depth_counts
        }
    
    def cleanup(self):
        """Cleanup resources"""
        if self.context:
            try:
                self.context.close()
            except:
                pass
        
        if self.browser:
            try:
                self.browser.close()
            except:
                pass
        
        if self.playwright:
            try:
                self.playwright.stop()
            except:
                pass
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

