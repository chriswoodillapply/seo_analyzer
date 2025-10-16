#!/usr/bin/env python3
"""
Complete SEO Analysis with Full Content Caching

Workflow:
1. Crawl site → Cache URLs
2. Fetch all pages → Cache HTML, CSS, metadata
3. Load from cache → Run tests instantly
4. Optional: Run axe-core & Lighthouse
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, 'src')

from src.core.crawl_cache import CrawlCache
from src.core.content_cache import ContentCache, save_crawl_with_content
from src.crawlers.url_crawler import URLCrawler
from src.core.content_fetcher import ContentFetcher
from src.core.test_registry import TestRegistry
from src.core.seo_test_executor import SEOTestExecutor
from src.reporters.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description='SEO Analysis with Full Content Caching')
    parser.add_argument('--url', required=True, help='Root URL to analyze')
    parser.add_argument('--depth', type=int, default=3, help='Crawl depth')
    parser.add_argument('--max-urls', type=int, default=100, help='Max URLs to crawl')
    parser.add_argument('--use-cache', action='store_true', help='Use cached content if available')
    parser.add_argument('--max-age', type=int, default=24, help='Max cache age in hours')
    parser.add_argument('--save-css', action='store_true', help='Save CSS files in cache')
    parser.add_argument('--format', choices=['csv', 'excel', 'html'], default='csv')
    
    args = parser.parse_args()
    
    print('='*80)
    print('  SEO ANALYSIS WITH FULL CONTENT CACHING')
    print('='*80)
    
    content_cache = ContentCache()
    
    # Check if we have cached content
    if args.use_cache:
        print('\n[1] Checking content cache...')
        cached_urls = content_cache.get_cached_urls(args.url)
        stats = content_cache.get_cache_stats(args.url)
        
        if cached_urls:
            print(f'   Found {len(cached_urls)} cached pages')
            print(f'   Total cache size: {stats["total_size_mb"]:.2f} MB')
            print(f'   Cached at: {stats.get("newest_cache", "unknown")}')
            
            # Load content from cache
            print('\n[2] Loading content from cache...')
            contents = []
            for url in cached_urls:
                content = content_cache.load_content(args.url, url, args.max_age)
                if content:
                    contents.append(content)
            
            print(f'   Loaded {len(contents)} pages from cache')
        else:
            print('   No cached content found')
            contents = None
    else:
        contents = None
    
    # If no cache, crawl and fetch
    if not contents:
        print('\n[1] Crawling site...')
        crawler = URLCrawler(max_depth=args.depth, max_urls=args.max_urls)
        urls = crawler.crawl(args.url)
        print(f'   Discovered {len(urls)} URLs')
        
        print('\n[2] Fetching content for all pages...')
        fetcher = ContentFetcher(enable_javascript=True)
        contents = []
        
        for i, url in enumerate(urls, 1):
            print(f'   [{i}/{len(urls)}] Fetching {url}')
            try:
                content = fetcher.fetch_complete(url)
                contents.append(content)
            except Exception as e:
                print(f'      Error: {e}')
        
        # Save to cache
        print('\n[3] Saving content to cache...')
        save_crawl_with_content(args.url, contents, save_css=args.save_css)
    
    # Run tests
    print(f'\n[4] Running tests on {len(contents)} pages...')
    registry = TestRegistry()
    registry.discover_and_register('src.tests')
    executor = SEOTestExecutor(registry)
    
    print(f'   Registered {registry.get_test_count()} tests')
    
    all_results = []
    for i, content in enumerate(contents, 1):
        if i % 10 == 0:
            print(f'   Testing page {i}/{len(contents)}...')
        
        results = executor.execute_all_tests(content)
        all_results.extend(results)
    
    # Generate report
    print(f'\n[5] Generating {args.format.upper()} report...')
    generator = ReportGenerator(output_dir='output')
    
    if args.format == 'csv':
        report_path = generator.generate_csv([r.to_dict() for r in all_results])
    elif args.format == 'excel':
        report_path = generator.generate_excel([r.to_dict() for r in all_results])
    else:
        report_path = generator.generate_html_report([r.to_dict() for r in all_results])
    
    print(f'   Report saved: {report_path}')
    
    # Summary
    from collections import Counter
    from src.core.test_interface import TestStatus
    
    status_counts = Counter(r.status for r in all_results)
    
    print('\n' + '='*80)
    print('  SUMMARY')
    print('='*80)
    print(f'Pages analyzed:   {len(contents)}')
    print(f'Total tests run:  {len(all_results)}')
    print(f'Passed:           {status_counts.get(TestStatus.PASS, 0)}')
    print(f'Failed:           {status_counts.get(TestStatus.FAIL, 0)}')
    print(f'Warnings:         {status_counts.get(TestStatus.WARNING, 0)}')
    print(f'Info:             {status_counts.get(TestStatus.INFO, 0)}')
    print('='*80)
    
    print('\n💡 TIP: Next time, use --use-cache to run tests instantly!')
    print('='*80 + '\n')


if __name__ == '__main__':
    main()

