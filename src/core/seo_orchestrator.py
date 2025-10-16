#!/usr/bin/env python3
"""
SEOOrchestrator - Main coordinator for enterprise SEO analysis
"""

from typing import List, Dict, Any, Optional
from .content_fetcher import ContentFetcher, PageContent
from .seo_test_executor import SEOTestExecutor
from .test_interface import TestResult
from .test_registry import TestRegistry
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
        verbose: bool = False
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
        """
        self.user_agent = user_agent
        self.timeout = timeout
        self.headless = headless
        self.enable_javascript = enable_javascript
        self.output_dir = output_dir
        self.verbose = verbose
        
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
        
        # Results storage
        self.all_results: List[Dict[str, Any]] = []
        self.analyzed_urls: List[str] = []
    
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
        
        # Fetch content
        if self.verbose:
            print(f"  > Fetching static content...")
        page_content = self.content_fetcher.fetch_complete(url)
        
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
            results = self.test_executor.execute_specific_tests(page_content, test_ids)
        else:
            results = self.test_executor.execute_all_tests(page_content)
        
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
    
    def analyze_multiple_urls(
        self,
        urls: List[str],
        test_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze multiple URLs
        
        Args:
            urls: List of URLs to analyze
            test_ids: Optional list of specific test IDs to run
            
        Returns:
            Summary dictionary with statistics
        """
        print(f"\n=== Analyzing {len(urls)} URLs ===\n")
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] ", end="")
            
            try:
                results = self.analyze_single_url(url, test_ids)
                if results:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  Error: {e}")
                failed += 1
        
        summary = {
            'total_urls': len(urls),
            'successful': successful,
            'failed': failed,
            'total_tests': len(self.all_results),
            'analyzed_urls': self.analyzed_urls
        }
        
        print(f"\n=== Analysis Complete ===")
        print(f"URLs analyzed: {successful}/{len(urls)}")
        print(f"Total tests executed: {len(self.all_results)}\n")
        
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
        
        # Crawl for URLs
        with URLCrawler(
            max_depth=max_depth,
            max_urls=max_urls,
            use_javascript=self.enable_javascript,
            timeout=self.timeout,
            user_agent=self.user_agent
        ) as crawler:
            discovered_urls = crawler.crawl(start_urls)
            stats = crawler.get_statistics()
        
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
    
    def cleanup(self):
        """Cleanup resources"""
        self.content_fetcher.cleanup()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

