#!/usr/bin/env python3
"""
SEOOrchestrator - Main coordinator for enterprise SEO analysis
"""

from typing import List, Dict, Any, Optional
from .content_fetcher import ContentFetcher, PageContent
from .seo_test_executor import SEOTestExecutor
from .test_interface import TestResult
from .test_registry import TestRegistry
from .content_cache import ContentCache
from .crawl_cache import CrawlCache
from .crawl_context import CrawlContext, build_crawl_context_from_results
from ..crawlers.url_crawler import URLCrawler
from ..reporters.report_generator import ReportGenerator


class SEOOrchestrator:
    """
    Enterprise SEO orchestrator that coordinates:
    - URL discovery/crawling
    - Content fetching (static + rendered)
    - Test execution
    - Report generation
    """
    
    def __init__(
        self,
        user_agent: Optional[str] = None,
        timeout: int = 30,
        headless: bool = True,
        enable_javascript: bool = True,
        output_dir: str = 'output',
        verbose: bool = False,
        enable_caching: bool = True,
        cache_max_age_hours: int = 24,
        save_css: bool = True,
        force_refresh: bool = False
    ):
        """
        Initialize SEO Orchestrator
        
        Args:
            user_agent: Custom user agent string
            timeout: Request timeout in seconds
            headless: Run browser in headless mode
            enable_javascript: Enable JavaScript rendering
            output_dir: Output directory for reports
            verbose: Enable verbose logging
            enable_caching: Enable content and crawl caching (default: True)
            cache_max_age_hours: Maximum cache age in hours (default: 24)
            save_css: Save CSS files in cache (default: True)
            force_refresh: Force refresh all content, bypassing cache (default: False)
        """
        self.user_agent = user_agent
        self.timeout = timeout
        self.headless = headless
        self.enable_javascript = enable_javascript
        self.output_dir = output_dir
        self.verbose = verbose
        self.enable_caching = enable_caching
        self.cache_max_age_hours = cache_max_age_hours
        self.save_css = save_css
        self.force_refresh = force_refresh
        
        # Initialize components
        self.content_fetcher = ContentFetcher(
            user_agent=user_agent,
            timeout=timeout,
            headless=headless,
            enable_javascript=enable_javascript
        )
        
        # Use the plugin-based executor by default. Auto-discover tests
        registry = TestRegistry()
        try:
            registry.discover_and_register('src.tests')
        except Exception:
            # If discovery fails, continue with an empty registry
            pass

        self.test_executor = SEOTestExecutor(registry)
        self.report_generator = ReportGenerator(output_dir=output_dir)
        
        # Initialize caching components if enabled
        if self.enable_caching:
            self.content_cache = ContentCache(f"{output_dir}/content_cache")
            self.crawl_cache = CrawlCache(f"{output_dir}/crawl_cache")
            if self.verbose:
                print(f"✅ Caching enabled - Content: {self.content_cache.cache_dir}, Crawl: {self.crawl_cache.cache_dir}")
        else:
            self.content_cache = None
            self.crawl_cache = None
            if self.verbose:
                print("⚠️  Caching disabled")
        
        # Results storage
        self.all_results: List[Dict[str, Any]] = []
        self.analyzed_urls: List[str] = []
        self.crawl_context: Optional[CrawlContext] = None
    
    def analyze_single_url(
        self,
        url: str,
        test_ids: Optional[List[str]] = None
    ) -> List[TestResult]:
        """
        Analyze a single URL
        
        Args:
            url: URL to analyze
            test_ids: Optional list of specific test IDs to run
            
        Returns:
            List of test results
        """
        print(f"Analyzing: {url}")
        
        # Check cache first if caching is enabled and not forcing refresh
        page_content = None
        if self.enable_caching and self.content_cache and not self.force_refresh:
            if self.verbose:
                print(f"  > Checking content cache...")
            # Extract root URL for cache lookup
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            page_content = self.content_cache.load_content(root_url, url, max_age_hours=self.cache_max_age_hours)
            if page_content:
                if self.verbose:
                    print(f"  > Using cached content")
            else:
                if self.verbose:
                    print(f"  > No valid cache found, fetching fresh content...")
        elif self.force_refresh:
            if self.verbose:
                print(f"  > Force refresh enabled, bypassing cache...")
        
        # Fetch content if not cached
        if page_content is None:
            if self.verbose:
                print(f"  > Fetching static content...")
            page_content = self.content_fetcher.fetch_complete(url)
            
            # Cache the content if caching is enabled
            if self.enable_caching and self.content_cache and not page_content.error:
                if self.verbose:
                    print(f"  > Caching content...")
                self.content_cache.save_content(root_url, page_content, save_css=self.save_css)
        
        if page_content.error:
            print(f"  Error fetching content: {page_content.error}")
            return []
        
        if self.verbose:
            print(f"  > Static HTML: {len(page_content.static_html)} bytes")
            if page_content.rendered_html:
                print(f"  > Rendered HTML: {len(page_content.rendered_html)} bytes")
                print(f"  > Load time: {page_content.static_load_time:.2f}s")
        
        # Execute tests
        if self.verbose:
            print(f"  > Running SEO tests...")
        if test_ids:
            results = self.test_executor.execute_specific_tests(page_content, test_ids, self.crawl_context)
        else:
            results = self.test_executor.execute_all_tests(page_content, self.crawl_context)
        
        if self.verbose:
            passed = len([r for r in results if r.status.value == 'Pass'])
            failed = len([r for r in results if r.status.value == 'Fail'])
            warnings = len([r for r in results if r.status.value == 'Warning'])
            print(f"  > Results: {passed} passed, {failed} failed, {warnings} warnings")
        
        print(f"  Completed {len(results)} tests")
        
        # Store results
        self.analyzed_urls.append(url)
        result_dicts = [result.to_dict() for result in results]
        self.all_results.extend(result_dicts)
        
        return results
    
    def _extract_title_from_results(self, results: List[TestResult]) -> Optional[str]:
        """Extract page title from test results"""
        # Look for title in meta tags test results
        for result in results:
            if hasattr(result, 'test_id') and 'title' in result.test_id.lower():
                if hasattr(result, 'issue_description'):
                    return result.issue_description
        return None
    
    def _extract_word_count_from_results(self, results: List[TestResult]) -> int:
        """Extract word count from test results"""
        # Look for word count in content test results
        for result in results:
            if hasattr(result, 'test_id') and 'word_count' in result.test_id.lower():
                if hasattr(result, 'score') and result.score:
                    try:
                        return int(result.score)
                    except:
                        pass
        return 0
    
    def _extract_internal_links_from_results(self, results: List[TestResult]) -> List[str]:
        """Extract internal links from test results"""
        internal_links = []
        for result in results:
            if hasattr(result, 'test_id') and 'internal_links' in result.test_id.lower():
                if hasattr(result, 'issue_description'):
                    # Parse links from issue description
                    # This is a simplified extraction - in practice, you'd parse the actual links
                    pass
        return internal_links
    
    def _extract_external_links_from_results(self, results: List[TestResult]) -> List[str]:
        """Extract external links from test results"""
        external_links = []
        for result in results:
            if hasattr(result, 'test_id') and 'external_links' in result.test_id.lower():
                if hasattr(result, 'issue_description'):
                    # Parse links from issue description
                    pass
        return external_links
    
    def _extract_links_from_content(self, page_content: PageContent) -> tuple[List[str], List[str]]:
        """Extract internal and external links from page content"""
        internal_links = []
        external_links = []
        
        try:
            soup = page_content.rendered_soup or page_content.static_soup
            if not soup:
                return internal_links, external_links
            
            # Get base URL for comparison
            from urllib.parse import urlparse, urljoin
            base_url = page_content.url
            base_domain = urlparse(base_url).netloc
            
            # Find all links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                if not href:
                    continue
                
                # Resolve relative URLs
                absolute_url = urljoin(base_url, href)
                link_domain = urlparse(absolute_url).netloc
                
                # Categorize as internal or external
                if link_domain == base_domain or not link_domain:
                    internal_links.append(absolute_url)
                else:
                    external_links.append(absolute_url)
                    
        except Exception as e:
            if self.verbose:
                print(f"  Error extracting links: {e}")
        
        return internal_links, external_links
    
    def _extract_title_from_content(self, page_content: PageContent) -> Optional[str]:
        """Extract page title from content"""
        try:
            soup = page_content.rendered_soup or page_content.static_soup
            if soup:
                title_tag = soup.find('title')
                if title_tag:
                    return title_tag.get_text().strip()
        except Exception:
            pass
        return None
    
    def _extract_word_count_from_content(self, page_content: PageContent) -> int:
        """Extract word count from content"""
        try:
            soup = page_content.rendered_soup or page_content.static_soup
            if soup:
                # Get text content
                text_content = soup.get_text()
                # Count words
                words = text_content.split()
                return len(words)
        except Exception:
            pass
        return 0
    
    def analyze_multiple_urls(
        self,
        urls: List[str],
        test_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze multiple URLs with proper two-phase approach:
        1. Fetch all content and build crawl context
        2. Run all tests with complete context
        
        Args:
            urls: List of URLs to analyze
            test_ids: Optional list of specific test IDs to run
            
        Returns:
            Summary dictionary with statistics
        """
        print(f"\n=== Analyzing {len(urls)} URLs ===\n")
        
        # PHASE 1: Fetch all content and build crawl context
        print("Phase 1: Fetching content and building site context...")
        self.crawl_context = CrawlContext(root_url=urls[0] if urls else "")
        
        successful_fetches = 0
        failed_fetches = 0
        all_page_content = {}  # Store all fetched content
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Fetching: {url}")
            
            try:
                # Fetch content (with or without caching)
                page_content = self.content_fetcher.fetch_complete(url)
                
                if page_content.error:
                    print(f"  Error: {page_content.error}")
                    failed_fetches += 1
                    continue
                
                successful_fetches += 1
                all_page_content[url] = page_content
                
                # Extract links and metadata
                internal_links, external_links = self._extract_links_from_content(page_content)
                
                # Add to crawl context
                from .crawl_context import PageMetadata
                metadata = PageMetadata(
                    url=url,
                    status_code=page_content.status_code,
                    title=self._extract_title_from_content(page_content),
                    word_count=self._extract_word_count_from_content(page_content)
                )
                self.crawl_context.add_page(url, metadata)
                
                # Add link relationships to crawl context
                for target_url in internal_links:
                    self.crawl_context.add_link(url, target_url, is_internal=True)
                for target_url in external_links:
                    self.crawl_context.add_link(url, target_url, is_internal=False)
                
                if self.verbose:
                    print(f"  Links: {len(internal_links)} internal, {len(external_links)} external")
                    
            except Exception as e:
                print(f"  Error: {e}")
                failed_fetches += 1
        
        # Finalize crawl context
        if self.crawl_context:
            self.crawl_context.finalize()
            if self.verbose:
                print(f"\n✅ Crawl context built:")
                print(f"  Total pages: {self.crawl_context.total_pages}")
                print(f"  Total links: {len(self.crawl_context.all_links)}")
                print(f"  Orphan pages: {len(self.crawl_context.orphan_pages)}")
        
        # PHASE 2: Run all tests with complete context
        print(f"\nPhase 2: Running SEO tests with complete site context...")
        successful_tests = 0
        failed_tests = 0
        
        for i, (url, page_content) in enumerate(all_page_content.items(), 1):
            print(f"[{i}/{len(all_page_content)}] Testing: {url}")
            
            try:
                # Run tests with complete crawl context
                if test_ids:
                    results = self.test_executor.execute_specific_tests(page_content, test_ids, self.crawl_context)
                else:
                    results = self.test_executor.execute_all_tests(page_content, self.crawl_context)
                
                if results:
                    successful_tests += 1
                    # Store results
                    self.analyzed_urls.append(url)
                    result_dicts = [result.to_dict() for result in results]
                    self.all_results.extend(result_dicts)
                    
                    if self.verbose:
                        passed = len([r for r in results if r.status.value == 'Pass'])
                        failed = len([r for r in results if r.status.value == 'Fail'])
                        warnings = len([r for r in results if r.status.value == 'Warning'])
                        print(f"  Results: {passed} passed, {failed} failed, {warnings} warnings")
                else:
                    failed_tests += 1
                    
            except Exception as e:
                print(f"  Error: {e}")
                failed_tests += 1
        
        summary = {
            'total_urls': len(urls),
            'successful': successful_tests,
            'failed': failed_tests,
            'total_tests': len(self.all_results),
            'analyzed_urls': self.analyzed_urls,
            'fetch_stats': {
                'successful_fetches': successful_fetches,
                'failed_fetches': failed_fetches
            }
        }
        
        print(f"\n=== Analysis Complete ===")
        print(f"Content fetched: {successful_fetches}/{len(urls)}")
        print(f"Tests executed: {successful_tests}/{len(all_page_content)}")
        print(f"Total tests: {len(self.all_results)}\n")
        
        return summary
    
    def analyze_with_crawling(
        self,
        start_urls: List[str],
        max_depth: int = 2,
        max_urls: int = 100,
        test_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Crawl websites and analyze discovered URLs
        
        Args:
            start_urls: Starting URLs for crawling
            max_depth: Maximum crawl depth
            max_urls: Maximum URLs to discover
            test_ids: Optional list of specific test IDs to run
            
        Returns:
            Summary dictionary with statistics
        """
        print(f"\n=== Starting URL Discovery ===")
        print(f"Start URLs: {len(start_urls)}")
        print(f"Max depth: {max_depth}")
        print(f"Max URLs: {max_urls}\n")
        
        # Check crawl cache first if caching is enabled and not forcing refresh
        discovered_urls = []
        stats = {}
        if self.enable_caching and self.crawl_cache and not self.force_refresh:
            if self.verbose:
                print("Checking crawl cache...")
            cached_crawl = self.crawl_cache.load_crawl(start_urls[0], max_urls, max_depth, max_age_hours=self.cache_max_age_hours)
            if cached_crawl:
                discovered_urls = cached_crawl['urls']
                stats = cached_crawl.get('metadata', {})
                if self.verbose:
                    print(f"Using cached crawl results: {len(discovered_urls)} URLs")
            else:
                if self.verbose:
                    print("No valid crawl cache found, crawling fresh...")
        elif self.force_refresh:
            if self.verbose:
                print("Force refresh enabled, bypassing crawl cache...")
        
        # Crawl for URLs if not cached
        if not discovered_urls:
            with URLCrawler(
                max_depth=max_depth,
                max_urls=max_urls,
                use_javascript=self.enable_javascript,
                timeout=self.timeout,
                user_agent=self.user_agent
            ) as crawler:
                discovered_urls = crawler.crawl(start_urls)
                stats = crawler.get_statistics()
            
            # Cache the crawl results if caching is enabled
            if self.enable_caching and self.crawl_cache:
                if self.verbose:
                    print("Caching crawl results...")
                self.crawl_cache.save_crawl(start_urls[0], discovered_urls, stats, max_urls, max_depth)
        
        print(f"Discovered {len(discovered_urls)} URLs\n")
        
        # Analyze discovered URLs
        summary = self.analyze_multiple_urls(discovered_urls, test_ids)
        summary['crawl_stats'] = stats
        
        return summary
    
    def generate_reports(
        self,
        formats: List[str] = ['csv', 'excel', 'json', 'html'],
        base_filename: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate reports in specified formats
        
        Args:
            formats: List of formats ('csv', 'excel', 'json', 'html')
            base_filename: Base filename for reports
            
        Returns:
            Dictionary of format -> filepath
        """
        if not self.all_results:
            print("No results to generate reports")
            return {}
        
        print(f"\n=== Generating Reports ===")
        
        generated_files = {}
        
        if 'csv' in formats:
            csv_file = self.report_generator.generate_csv_report(
                self.all_results,
                f"{base_filename}.csv" if base_filename else None
            )
            if csv_file:
                generated_files['csv'] = csv_file
        
        if 'excel' in formats:
            excel_file = self.report_generator.generate_excel_report(
                self.all_results,
                f"{base_filename}.xlsx" if base_filename else None
            )
            if excel_file:
                generated_files['excel'] = excel_file
        
        if 'json' in formats:
            json_file = self.report_generator.generate_json_report(
                self.all_results,
                f"{base_filename}.json" if base_filename else None
            )
            if json_file:
                generated_files['json'] = json_file
        
        if 'html' in formats:
            html_file = self.report_generator.generate_html_report(
                self.all_results,
                f"{base_filename}.html" if base_filename else None
            )
            if html_file:
                generated_files['html'] = html_file
        
        print(f"Generated {len(generated_files)} report(s)\n")
        
        return generated_files
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get all results"""
        return self.all_results
    
    def get_results_by_url(self, url: str) -> List[Dict[str, Any]]:
        """Get results for a specific URL"""
        return [r for r in self.all_results if r.get('URL') == url]
    
    def get_results_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get results by status (Pass, Fail, Warning, etc.)"""
        return [r for r in self.all_results if r.get('Status') == status]
    
    def get_results_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get results by category"""
        return [r for r in self.all_results if r.get('Category') == category]
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.all_results:
            return {}
        
        total = len(self.all_results)
        passed = len([r for r in self.all_results if r.get('Status') == 'Pass'])
        failed = len([r for r in self.all_results if r.get('Status') == 'Fail'])
        warnings = len([r for r in self.all_results if r.get('Status') == 'Warning'])
        
        # Group by category
        categories = {}
        for result in self.all_results:
            cat = result.get('Category', 'Unknown')
            if cat not in categories:
                categories[cat] = {'total': 0, 'passed': 0, 'failed': 0, 'warnings': 0}
            
            categories[cat]['total'] += 1
            status = result.get('Status')
            if status == 'Pass':
                categories[cat]['passed'] += 1
            elif status == 'Fail':
                categories[cat]['failed'] += 1
            elif status == 'Warning':
                categories[cat]['warnings'] += 1
        
        return {
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'urls_analyzed': len(self.analyzed_urls),
            'categories': categories
        }
    
    def print_summary(self):
        """Print a summary of results"""
        stats = self.get_summary_stats()
        
        if not stats:
            print("No results available")
            return
        
        print("\n" + "=" * 60)
        print("SEO ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"URLs Analyzed:     {stats['urls_analyzed']}")
        print(f"Total Tests:       {stats['total_tests']}")
        print(f"Passed:            {stats['passed']}")
        print(f"Failed:            {stats['failed']}")
        print(f"Warnings:          {stats['warnings']}")
        print(f"Pass Rate:         {stats['pass_rate']:.1f}%")
        print("\nBy Category:")
        print("-" * 60)
        
        for category, cat_stats in stats['categories'].items():
            print(f"{category:20} | Total: {cat_stats['total']:3} | "
                  f"Pass: {cat_stats['passed']:3} | "
                  f"Fail: {cat_stats['failed']:3} | "
                  f"Warn: {cat_stats['warnings']:3}")
        
        print("=" * 60 + "\n")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics if caching is enabled"""
        if not self.enable_caching:
            return {"caching_enabled": False}
        
        stats = {
            "caching_enabled": True,
            "content_cache": {},
            "crawl_cache": {}
        }
        
        if self.content_cache:
            try:
                content_stats = self.content_cache.get_cache_stats()
                stats["content_cache"] = content_stats
            except Exception as e:
                stats["content_cache"] = {"error": str(e)}
        
        if self.crawl_cache:
            try:
                crawl_stats = self.crawl_cache.get_cache_stats()
                stats["crawl_cache"] = crawl_stats
            except Exception as e:
                stats["crawl_cache"] = {"error": str(e)}
        
        return stats
    
    def clear_cache(self, content: bool = True, crawl: bool = True):
        """Clear cache if caching is enabled"""
        if not self.enable_caching:
            print("Caching is disabled")
            return
        
        if content and self.content_cache:
            try:
                self.content_cache.clear_cache()
                print("✅ Content cache cleared")
            except Exception as e:
                print(f"❌ Error clearing content cache: {e}")
        
        if crawl and self.crawl_cache:
            try:
                self.crawl_cache.clear_cache()
                print("✅ Crawl cache cleared")
            except Exception as e:
                print(f"❌ Error clearing crawl cache: {e}")
    
    def invalidate_cache(self):
        """Invalidate cache by setting force_refresh to True"""
        self.force_refresh = True
        print("🔄 Cache invalidation enabled - all content will be fetched fresh")
    
    def cleanup(self):
        """Cleanup resources"""
        self.content_fetcher.cleanup()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

