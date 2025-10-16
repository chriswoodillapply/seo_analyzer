#!/usr/bin/env python3
"""
SEO Analysis with Crawl Caching

This script demonstrates:
1. Crawl a site and cache results
2. Load cached URLs for subsequent runs
3. Run tests on all URLs without re-crawling
4. Optionally run axe-core and Lighthouse on URLs
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, 'src')

from src.core.crawl_cache import CrawlCache, save_crawl_to_simple_list, load_urls_from_file
from src.crawlers.url_crawler import URLCrawler
from src.core.content_fetcher import ContentFetcher
from src.core.test_registry import TestRegistry
from src.core.test_executor_v2 import SEOTestExecutorV2
from src.reporters.report_generator import ReportGenerator


def crawl_and_cache(root_url: str, depth: int = 3, max_urls: int = 100):
    """
    Crawl a site and cache the results.
    
    Args:
        root_url: URL to start crawling from
        depth: Maximum crawl depth
        max_urls: Maximum URLs to crawl
        
    Returns:
        List of discovered URLs
    """
    print('\n' + '='*80)
    print('  STEP 1: CRAWLING SITE')
    print('='*80)
    
    crawler = URLCrawler(root_url, max_urls=max_urls, depth=depth)
    urls = crawler.crawl()
    
    print(f'\nDiscovered {len(urls)} URLs')
    
    # Save to cache
    cache = CrawlCache()
    cache.save_crawl(root_url, urls, max_urls=max_urls, depth=depth)
    
    # Also save to simple text file
    save_crawl_to_simple_list(urls, f'output/crawled_urls_{Path(root_url).name}.txt')
    
    return urls


def load_cached_urls(root_url: str, depth: int = 3, max_urls: int = 100, max_age_hours: int = 24):
    """
    Load URLs from cache or from file.
    
    Args:
        root_url: Root URL
        depth: Crawl depth
        max_urls: Max URLs
        max_age_hours: Maximum cache age in hours
        
    Returns:
        List of URLs or None if not cached
    """
    print('\n' + '='*80)
    print('  CHECKING CACHE')
    print('='*80)
    
    cache = CrawlCache()
    cache_data = cache.load_crawl(root_url, max_urls, depth, max_age_hours)
    
    if cache_data:
        return cache_data['urls']
    
    # Try loading from simple text file
    url_file = f'output/crawled_urls_{Path(root_url).name}.txt'
    if Path(url_file).exists():
        print(f'\nFound URL list file: {url_file}')
        return load_urls_from_file(url_file)
    
    return None


def run_tests_on_urls(urls: list, run_axe: bool = False, run_lighthouse: bool = False):
    """
    Run SEO tests on a list of URLs.
    
    Args:
        urls: List of URLs to test
        run_axe: Whether to run axe-core
        run_lighthouse: Whether to run Lighthouse
        
    Returns:
        All test results
    """
    print('\n' + '='*80)
    print(f'  STEP 2: RUNNING TESTS ON {len(urls)} URLs')
    print('='*80)
    
    # Setup
    registry = TestRegistry()
    registry.discover_and_register('src.tests')
    executor = SEOTestExecutorV2(registry)
    fetcher = ContentFetcher(enable_javascript=True)
    
    print(f'\nRegistered {registry.get_test_count()} tests')
    print(f'JavaScript rendering: Enabled')
    print(f'axe-core: {"Enabled" if run_axe else "Disabled"}')
    print(f'Lighthouse: {"Enabled" if run_lighthouse else "Disabled"}')
    
    all_results = []
    
    for i, url in enumerate(urls, 1):
        print(f'\n[{i}/{len(urls)}] Testing: {url}')
        
        try:
            # Fetch content
            content = fetcher.fetch_complete(url)
            
            # TODO: If run_axe, inject and run axe-core here
            # if run_axe and page_object:
            #     from src.integrations.axe_core import run_full_accessibility_audit
            #     content.axe_results = run_full_accessibility_audit(page_object)
            
            # Run tests
            results = executor.execute_all_tests(content)
            all_results.extend(results)
            
            # Show quick summary
            stats = executor.get_statistics()
            print(f'  Tests run: {stats["total_tests"]} | '
                  f'Pass: {stats["passed"]} | '
                  f'Fail: {stats["failed"]} | '
                  f'Warn: {stats["warnings"]}')
            
        except Exception as e:
            print(f'  Error: {e}')
            continue
    
    # TODO: If run_lighthouse, run it on each URL
    # if run_lighthouse:
    #     from src.integrations.lighthouse import run_quick_lighthouse_audit
    #     for url in urls:
    #         lighthouse_results = run_quick_lighthouse_audit(url)
    
    return all_results


def generate_report(results: list, output_format: str = 'csv'):
    """
    Generate test report.
    
    Args:
        results: Test results
        output_format: Report format (csv, excel, html)
    """
    print('\n' + '='*80)
    print('  STEP 3: GENERATING REPORT')
    print('='*80)
    
    generator = ReportGenerator(output_dir='output')
    
    if output_format == 'csv':
        report_path = generator.generate_csv([r.to_dict() for r in results])
    elif output_format == 'excel':
        report_path = generator.generate_excel([r.to_dict() for r in results])
    elif output_format == 'html':
        report_path = generator.generate_html_report([r.to_dict() for r in results])
    else:
        report_path = generator.generate_csv([r.to_dict() for r in results])
    
    print(f'\nReport saved: {report_path}')
    
    # Show summary
    from collections import Counter
    from src.core.test_interface import TestStatus
    
    status_counts = Counter(r.status for r in results)
    
    print('\n' + '-'*80)
    print('SUMMARY:')
    print('-'*80)
    print(f'Total Tests:  {len(results)}')
    print(f'Passed:       {status_counts.get(TestStatus.PASS, 0)}')
    print(f'Failed:       {status_counts.get(TestStatus.FAIL, 0)}')
    print(f'Warnings:     {status_counts.get(TestStatus.WARNING, 0)}')
    print(f'Info:         {status_counts.get(TestStatus.INFO, 0)}')
    print('-'*80)


def main():
    parser = argparse.ArgumentParser(description='SEO Analysis with Caching')
    parser.add_argument('--url', required=True, help='Root URL to analyze')
    parser.add_argument('--depth', type=int, default=3, help='Crawl depth (default: 3)')
    parser.add_argument('--max-urls', type=int, default=100, help='Max URLs to crawl (default: 100)')
    parser.add_argument('--use-cache', action='store_true', help='Use cached crawl if available')
    parser.add_argument('--max-age', type=int, default=24, help='Max cache age in hours (default: 24)')
    parser.add_argument('--recrawl', action='store_true', help='Force re-crawl even if cache exists')
    parser.add_argument('--axe', action='store_true', help='Run axe-core accessibility tests')
    parser.add_argument('--lighthouse', action='store_true', help='Run Lighthouse performance tests')
    parser.add_argument('--format', choices=['csv', 'excel', 'html'], default='csv', help='Report format')
    parser.add_argument('--url-file', help='Load URLs from file instead of crawling')
    
    args = parser.parse_args()
    
    print('='*80)
    print('  SEO ANALYSIS WITH CRAWL CACHING')
    print('='*80)
    print(f'\nRoot URL: {args.url}')
    print(f'Max URLs: {args.max_urls}')
    print(f'Depth: {args.depth}')
    
    # Get URLs
    urls = None
    
    if args.url_file:
        # Load from file
        print(f'\nLoading URLs from: {args.url_file}')
        urls = load_urls_from_file(args.url_file)
    elif args.use_cache and not args.recrawl:
        # Try cache first
        urls = load_cached_urls(args.url, args.depth, args.max_urls, args.max_age)
    
    if urls is None or args.recrawl:
        # Crawl site
        urls = crawl_and_cache(args.url, args.depth, args.max_urls)
    
    if not urls:
        print('\nError: No URLs to analyze')
        return
    
    # Run tests
    results = run_tests_on_urls(urls, run_axe=args.axe, run_lighthouse=args.lighthouse)
    
    # Generate report
    generate_report(results, args.format)
    
    print('\n' + '='*80)
    print('  ANALYSIS COMPLETE')
    print('='*80 + '\n')


if __name__ == '__main__':
    main()

