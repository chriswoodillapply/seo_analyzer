#!/usr/bin/env python3
"""
ContentFetcher - Handles fetching both static HTML and fully rendered content
"""

import time
from typing import Dict, Any, Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class PageContent:
    """Container for page content analysis"""
    url: str
    status_code: int
    
    # Static HTML content
    static_html: str
    static_soup: BeautifulSoup
    static_headers: Dict[str, str]
    static_load_time: float
    
    # Rendered content (JavaScript executed)
    rendered_html: Optional[str] = None
    rendered_soup: Optional[BeautifulSoup] = None
    rendered_load_time: Optional[float] = None
    
    # CSS content for analysis
    css_files: Dict[str, str] = None  # url -> css_content
    computed_styles: Dict[str, Dict[str, str]] = None  # selector -> {property: value}
    
    # Performance metrics
    performance_metrics: Dict[str, Any] = None
    core_web_vitals: Dict[str, float] = None
    # Accessibility (axe-core) results
    axe_results: Optional[Dict[str, Any]] = None
    
    # Error tracking
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.core_web_vitals is None:
            self.core_web_vitals = {}
        if self.css_files is None:
            self.css_files = {}
        if self.computed_styles is None:
            self.computed_styles = {}


class ContentFetcher:
    """
    Enterprise-grade content fetcher that retrieves both static and rendered versions
    of web pages for comprehensive SEO analysis.
    """
    
    def __init__(
        self,
        user_agent: Optional[str] = None,
        timeout: int = 30,
        headless: bool = True,
        enable_javascript: bool = True
    ):
        """
        Initialize ContentFetcher
        
        Args:
            user_agent: Custom user agent string
            timeout: Request timeout in seconds
            headless: Run browser in headless mode
            enable_javascript: Enable JavaScript rendering with Playwright
        """
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
        self.timeout = timeout
        self.headless = headless
        self.enable_javascript = enable_javascript and PLAYWRIGHT_AVAILABLE
        
        # Setup session for static requests
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        # Playwright components (initialized on demand)
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        
        if self.enable_javascript:
            self._initialize_playwright()
    
    def _initialize_playwright(self):
        """Initialize Playwright for JavaScript rendering"""
        if not PLAYWRIGHT_AVAILABLE:
            return
        
        try:
            # Check if we're in an asyncio event loop
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                # We're in an event loop - try using nest_asyncio to allow nested loops
                try:
                    import nest_asyncio
                    nest_asyncio.apply()
                    print("Applied nest_asyncio to allow Playwright in async context")
                except ImportError:
                    print("Note: Install nest_asyncio for better async compatibility: pip install nest_asyncio")
                    # Continue anyway, might work
            except RuntimeError:
                # No event loop running, safe to use sync API
                pass
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security'
                ]
            )
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=self.user_agent
            )
            print("Playwright initialized successfully for JavaScript rendering")
        except Exception as e:
            print(f"Warning: Could not initialize Playwright: {e}")
            self.enable_javascript = False
    
    def fetch_static_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch static HTML content without JavaScript execution
        
        Args:
            url: URL to fetch
            
        Returns:
            Dictionary containing static content and metadata
        """
        start_time = time.time()
        
        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            load_time = time.time() - start_time
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'url': url,
                'status_code': response.status_code,
                'html': response.text,
                'soup': soup,
                'headers': dict(response.headers),
                'load_time': load_time,
                'final_url': response.url,
                'error': None
            }
            
        except Exception as e:
            return {
                'url': url,
                'status_code': 0,
                'html': '',
                'soup': None,
                'headers': {},
                'load_time': time.time() - start_time,
                'final_url': url,
                'error': str(e)
            }
    
    def fetch_rendered_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch JavaScript-rendered content using Playwright
        
        Args:
            url: URL to fetch
            
        Returns:
            Dictionary containing rendered content and performance metrics
        """
        if not self.enable_javascript or not self.context:
            return {
                'html': None,
                'soup': None,
                'load_time': None,
                'performance_metrics': {},
                'core_web_vitals': {},
                'error': 'JavaScript rendering not available'
            }
        
        start_time = time.time()
        
        try:
            page = self.context.new_page()
            
            # Set up Core Web Vitals monitoring BEFORE navigation
            # This is critical because LCP entries aren't buffered and must be observed in real-time
            page.add_init_script('''() => {
                window.__cwvMetrics = { lcp: null, fcp: null, cls: 0, fid: null };
                
                // Largest Contentful Paint - must observe, not query later
                if (PerformanceObserver.supportedEntryTypes.includes('largest-contentful-paint')) {
                    const lcpObserver = new PerformanceObserver((list) => {
                        const entries = list.getEntries();
                        const lastEntry = entries[entries.length - 1];
                        window.__cwvMetrics.lcp = {
                            value: lastEntry.startTime / 1000,
                            element: lastEntry.element ? lastEntry.element.tagName : 'unknown',
                            size: lastEntry.size || 0
                        };
                    });
                    lcpObserver.observe({ entryTypes: ['largest-contentful-paint'], buffered: true });
                }
                
                // First Contentful Paint
                if (PerformanceObserver.supportedEntryTypes.includes('paint')) {
                    const fcpObserver = new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (entry.name === 'first-contentful-paint') {
                                window.__cwvMetrics.fcp = entry.startTime / 1000;
                            }
                        }
                    });
                    fcpObserver.observe({ entryTypes: ['paint'], buffered: true });
                }
                
                // Cumulative Layout Shift
                if (PerformanceObserver.supportedEntryTypes.includes('layout-shift')) {
                    const clsObserver = new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (!entry.hadRecentInput) {
                                window.__cwvMetrics.cls += entry.value;
                            }
                        }
                    });
                    clsObserver.observe({ entryTypes: ['layout-shift'], buffered: true });
                }
                
                // First Input Delay
                if (PerformanceObserver.supportedEntryTypes.includes('first-input')) {
                    const fidObserver = new PerformanceObserver((list) => {
                        const firstInput = list.getEntries()[0];
                        if (firstInput) {
                            window.__cwvMetrics.fid = firstInput.processingStart - firstInput.startTime;
                        }
                    });
                    fidObserver.observe({ entryTypes: ['first-input'], buffered: true });
                }
            }''')
            
            # Also set up the metrics object immediately after page creation
            page.evaluate('''() => {
                if (!window.__cwvMetrics) {
                    window.__cwvMetrics = { lcp: null, fcp: null, cls: 0, fid: null };
                }
            }''')
            
            # Navigate to page
            response = page.goto(
                url,
                timeout=self.timeout * 1000,
                wait_until='networkidle'
            )
            
            # Wait for LCP to stabilize (Google recommends 3-5 seconds)
            # LCP changes as larger elements load, so we need to wait for:
            # 1. All images to load (especially hero images)
            # 2. Lazy-loaded content
            # 3. Dynamic content injected by JavaScript
            page.wait_for_timeout(10000)  # Increased to 10s for better LCP capture
            
            # Get Core Web Vitals from the observers we set up
            core_web_vitals = page.evaluate('() => window.__cwvMetrics')
            
            # Fallback: If observers didn't work, try to get Core Web Vitals directly
            if not core_web_vitals or all(v is None for v in core_web_vitals.values() if isinstance(v, (int, float))):
                core_web_vitals = page.evaluate('''() => {
                    const metrics = {};
                    
                    // Try to get LCP from performance entries
                    const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
                    if (lcpEntries.length > 0) {
                        const lcp = lcpEntries[lcpEntries.length - 1];
                        metrics.lcp = {
                            value: lcp.startTime / 1000,
                            element: lcp.element ? lcp.element.tagName : 'unknown',
                            size: lcp.size || 0
                        };
                    }
                    
                    // Try to get FCP from performance entries
                    const fcpEntries = performance.getEntriesByType('paint');
                    for (const entry of fcpEntries) {
                        if (entry.name === 'first-contentful-paint') {
                            metrics.fcp = entry.startTime / 1000;
                            break;
                        }
                    }
                    
                    // Try to get CLS from performance entries
                    const clsEntries = performance.getEntriesByType('layout-shift');
                    let cls = 0;
                    for (const entry of clsEntries) {
                        if (!entry.hadRecentInput) {
                            cls += entry.value;
                        }
                    }
                    metrics.cls = cls;
                    
                    // Try to get FID from performance entries
                    const fidEntries = performance.getEntriesByType('first-input');
                    if (fidEntries.length > 0) {
                        const fid = fidEntries[0];
                        metrics.fid = fid.processingStart - fid.startTime;
                    }
                    
                    return metrics;
                }''')
            
            # Run axe-core accessibility scan before reading content
            axe_results = None
            try:
                # Import locally to avoid import overhead when JS is disabled
                from ..integrations.axe_core import AxeCoreIntegration
                if AxeCoreIntegration.inject_axe_core(page):
                    axe_results = AxeCoreIntegration.run_axe_scan(page)
            except Exception as e:
                # Non-fatal; continue without axe results
                axe_results = None

            # Get rendered HTML
            rendered_html = page.content()
            rendered_soup = BeautifulSoup(rendered_html, 'html.parser')
            
            # Get performance metrics
            performance_metrics = page.evaluate('''() => {
                const perfEntries = performance.getEntriesByType('navigation');
                if (perfEntries.length > 0) {
                    const nav = perfEntries[0];
                    return {
                        domContentLoaded: nav.domContentLoadedEventEnd - nav.domContentLoadedEventStart,
                        loadComplete: nav.loadEventEnd - nav.loadEventStart,
                        dnsLookup: nav.domainLookupEnd - nav.domainLookupStart,
                        tcpConnect: nav.connectEnd - nav.connectStart,
                        serverResponse: nav.responseEnd - nav.responseStart,
                        domComplete: nav.domComplete - nav.navigationStart,
                        domInteractive: nav.domInteractive - nav.navigationStart
                    };
                }
                return {};
            }''')
            
            load_time = time.time() - start_time
            
            # Don't close the page yet - we need it for computed styles
            # Store page reference for later cleanup
            return {
                'html': rendered_html,
                'soup': rendered_soup,
                'load_time': load_time,
                'performance_metrics': performance_metrics,
                'core_web_vitals': core_web_vitals,
                'axe_results': axe_results,
                'status_code': response.status if response else 0,
                'page': page,  # Return page object for computed styles
                'error': None
            }
            
        except Exception as e:
            return {
                'html': None,
                'soup': None,
                'load_time': time.time() - start_time,
                'performance_metrics': {},
                'core_web_vitals': {},
                'axe_results': None,
                'status_code': 0,
                'error': str(e)
            }
    
    def _measure_core_web_vitals(self, page: Page) -> Dict[str, float]:
        """Measure Core Web Vitals using browser APIs"""
        try:
            # Use Performance Timeline API to get metrics that already occurred
            cwv = page.evaluate('''() => {
                const metrics = {};
                
                // Get Largest Contentful Paint (LCP)
                try {
                    const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
                    if (lcpEntries.length > 0) {
                        // Get the most recent LCP entry (it updates as larger elements load)
                        const lcpEntry = lcpEntries[lcpEntries.length - 1];
                        metrics.lcp = lcpEntry.startTime / 1000; // Convert to seconds
                        // Also capture the element details for debugging
                        metrics.lcpElement = lcpEntry.element ? lcpEntry.element.tagName : 'unknown';
                        metrics.lcpSize = lcpEntry.size || 0;
                    }
                } catch (e) {
                    // LCP not available in this browser
                    console.log('LCP not available:', e.message);
                }
                
                // Get First Contentful Paint (FCP)
                try {
                    const paintEntries = performance.getEntriesByType('paint');
                    const fcpEntry = paintEntries.find(entry => entry.name === 'first-contentful-paint');
                    if (fcpEntry) {
                        metrics.fcp = fcpEntry.startTime / 1000; // Convert to seconds
                    }
                } catch (e) {
                    // FCP not available
                }
                
                // Calculate Cumulative Layout Shift (CLS)
                try {
                    const clsEntries = performance.getEntriesByType('layout-shift');
                    let cls = 0;
                    for (const entry of clsEntries) {
                        // Only count layout shifts without recent user input
                        if (!entry.hadRecentInput) {
                            cls += entry.value;
                        }
                    }
                    metrics.cls = cls;
                } catch (e) {
                    // CLS not available
                }
                
                // Get Time to First Byte (TTFB) - bonus metric
                try {
                    const navEntries = performance.getEntriesByType('navigation');
                    if (navEntries.length > 0) {
                        metrics.ttfb = navEntries[0].responseStart / 1000; // Convert to seconds
                    }
                } catch (e) {
                    // TTFB not available
                }
                
                // Get DOM Content Loaded - bonus metric
                try {
                    const navEntries = performance.getEntriesByType('navigation');
                    if (navEntries.length > 0) {
                        metrics.domContentLoaded = navEntries[0].domContentLoadedEventEnd / 1000;
                    }
                } catch (e) {
                    // DCL not available
                }
                
                return metrics;
            }''')
            return cwv if cwv else {}
        except Exception as e:
            print(f"Error measuring Core Web Vitals: {e}")
            return {}
    
    def extract_css_files(self, soup: BeautifulSoup, base_url: str) -> Dict[str, str]:
        """
        Extract and fetch all CSS files referenced in the page
        
        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links
            
        Returns:
            Dictionary of CSS URL -> CSS content
        """
        css_files = {}
        
        try:
            # Find all CSS links
            css_links = soup.find_all('link', rel='stylesheet')
            css_links.extend(soup.find_all('style', type='text/css'))
            
            for link in css_links:
                css_url = None
                css_content = None
                
                if link.name == 'link':
                    # External CSS file
                    href = link.get('href')
                    if href:
                        css_url = self._resolve_url(href, base_url)
                        try:
                            response = requests.get(css_url, timeout=self.timeout, headers=self.session.headers)
                            if response.status_code == 200:
                                css_content = response.text
                        except Exception as e:
                            print(f"Error fetching CSS {css_url}: {e}")
                            continue
                
                elif link.name == 'style':
                    # Inline CSS
                    css_url = f"{base_url}#inline-css"
                    css_content = link.get_text()
                
                if css_url and css_content:
                    css_files[css_url] = css_content
                    
        except Exception as e:
            print(f"Error extracting CSS files: {e}")
        
        return css_files
    
    def get_computed_styles(self, page: 'Page') -> Dict[str, Dict[str, str]]:
        """
        Get computed styles for elements using Playwright
        
        Args:
            page: Playwright page object
            
        Returns:
            Dictionary of selector -> {property: value}
        """
        try:
            # Get computed styles for common elements
            selectors = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'p', 'a', 'button', 'input', 'img',
                'nav', 'header', 'footer', 'main',
                '.btn', '.button', '.link', '.text'
            ]
            
            computed_styles = {}
            
            for selector in selectors:
                try:
                    elements = page.query_selector_all(selector)
                    if elements:
                        # Get styles for first element of each type
                        element = elements[0]
                        styles = page.evaluate('''(element) => {
                            const computed = window.getComputedStyle(element);
                            const result = {};
                            for (let prop of computed) {
                                result[prop] = computed.getPropertyValue(prop);
                            }
                            return result;
                        }''', element)
                        
                        if styles:
                            computed_styles[selector] = styles
                            
                except Exception as e:
                    continue  # Skip this selector if it fails
            
            return computed_styles
            
        except Exception as e:
            print(f"Error getting computed styles: {e}")
            return {}
    
    def _resolve_url(self, url: str, base_url: str) -> str:
        """Resolve relative URL to absolute URL"""
        from urllib.parse import urljoin
        return urljoin(base_url, url)
    
    def fetch_complete(self, url: str) -> PageContent:
        """
        Fetch both static and rendered content for comprehensive analysis
        
        Args:
            url: URL to analyze
            
        Returns:
            PageContent object containing all fetched data
        """
        # Fetch static content first
        static_data = self.fetch_static_content(url)
        
        if static_data['error']:
            return PageContent(
                url=url,
                status_code=static_data['status_code'],
                static_html='',
                static_soup=None,
                static_headers={},
                static_load_time=static_data['load_time'],
                error=static_data['error']
            )
        
        # Extract CSS files from static content
        css_files = self.extract_css_files(static_data['soup'], url)
        
        # Fetch rendered content if enabled
        rendered_data = None
        computed_styles = {}
        if self.enable_javascript:
            rendered_data = self.fetch_rendered_content(url)
            # Get computed styles from rendered page
            if rendered_data and 'page' in rendered_data:
                computed_styles = self.get_computed_styles(rendered_data['page'])
                # Close the page after getting computed styles
                try:
                    rendered_data['page'].close()
                except:
                    pass
        
        return PageContent(
            url=url,
            status_code=static_data['status_code'],
            static_html=static_data['html'],
            static_soup=static_data['soup'],
            static_headers=static_data['headers'],
            static_load_time=static_data['load_time'],
            rendered_html=rendered_data['html'] if rendered_data else None,
            rendered_soup=rendered_data['soup'] if rendered_data else None,
            rendered_load_time=rendered_data['load_time'] if rendered_data else None,
            css_files=css_files,
            computed_styles=computed_styles,
            performance_metrics=rendered_data['performance_metrics'] if rendered_data else {},
            core_web_vitals=rendered_data['core_web_vitals'] if rendered_data else {},
            axe_results=rendered_data['axe_results'] if rendered_data else None,
            error=None
        )
    
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
        
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

