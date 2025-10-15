#!/usr/bin/env python3
"""
Enterprise SEO Analysis Tool - Main Entry Point

Usage:
  # Analyze single URL
  python seo_analysis.py --url https://example.com
  
  # Analyze multiple URLs
  python seo_analysis.py --urls https://example.com https://test.com
  
  # Analyze URLs from file
  python seo_analysis.py --url-file urls.txt
  
  # Crawl and analyze
  python seo_analysis.py --url https://example.com --crawl --depth 3 --max-urls 100
  
  # Generate specific report formats
  python seo_analysis.py --url https://example.com --formats csv excel
"""

import argparse
import sys
import os

# Fix Windows console encoding issues
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding for stdout/stderr
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # If that fails, replace errors instead of crashing
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

from src import SEOOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description='Enterprise SEO Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # URL input options
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument(
        '--url',
        type=str,
        help='Single URL to analyze'
    )
    url_group.add_argument(
        '--urls',
        nargs='+',
        help='Multiple URLs to analyze'
    )
    url_group.add_argument(
        '--url-file',
        type=str,
        help='File containing URLs (one per line)'
    )
    
    # Crawling options
    parser.add_argument(
        '--crawl',
        action='store_true',
        help='Enable URL crawling/discovery'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=2,
        help='Crawl depth (default: 2)'
    )
    parser.add_argument(
        '--max-urls',
        type=int,
        default=100,
        help='Maximum URLs to discover (default: 100)'
    )
    
    # Analysis options
    parser.add_argument(
        '--no-javascript',
        action='store_true',
        help='Disable JavaScript rendering (faster but less complete)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--user-agent',
        type=str,
        help='Custom user agent string'
    )
    
    # Report options
    parser.add_argument(
        '--formats',
        nargs='+',
        choices=['csv', 'excel', 'json', 'html'],
        default=['csv', 'excel'],
        help='Report formats to generate (default: csv excel)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output directory for reports (default: output)'
    )
    parser.add_argument(
        '--filename',
        type=str,
        help='Base filename for reports (without extension)'
    )
    
    # Other options
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Collect URLs
    urls = []
    if args.url:
        urls = [args.url]
    elif args.urls:
        urls = args.urls
    elif args.url_file:
        try:
            with open(args.url_file, 'r', encoding='utf-8') as f:
                urls = [
                    line.strip() 
                    for line in f 
                    if line.strip() and not line.strip().startswith('#')
                ]
        except FileNotFoundError:
            print(f"Error: File '{args.url_file}' not found")
            sys.exit(1)
    
    if not urls:
        print("Error: No URLs provided")
        sys.exit(1)
    
    # Validate URLs
    valid_urls = [url for url in urls if url.startswith(('http://', 'https://'))]
    if len(valid_urls) < len(urls):
        print(f"Warning: Skipped {len(urls) - len(valid_urls)} invalid URLs")
    
    if not valid_urls:
        print("Error: No valid URLs found")
        sys.exit(1)
    
    print(f"\n{'=' * 70}")
    print(f" Enterprise SEO Analysis")
    print(f"{'=' * 70}")
    print(f"URLs to analyze: {len(valid_urls)}")
    print(f"Crawling: {'Enabled' if args.crawl else 'Disabled'}")
    print(f"JavaScript: {'Enabled' if not args.no_javascript else 'Disabled'}")
    print(f"Report formats: {', '.join(args.formats)}")
    print(f"{'=' * 70}\n")
    
    try:
        # Initialize orchestrator
        with SEOOrchestrator(
            user_agent=args.user_agent,
            timeout=args.timeout,
            headless=args.headless,
            enable_javascript=not args.no_javascript,
            output_dir=args.output_dir,
            verbose=args.verbose
        ) as orchestrator:
            
            # Run analysis
            if args.crawl:
                summary = orchestrator.analyze_with_crawling(
                    start_urls=valid_urls,
                    max_depth=args.depth,
                    max_urls=args.max_urls
                )
            else:
                summary = orchestrator.analyze_multiple_urls(valid_urls)
            
            # Print summary
            orchestrator.print_summary()
            
            # Generate reports
            if orchestrator.all_results:
                files = orchestrator.generate_reports(
                    formats=args.formats,
                    base_filename=args.filename
                )
                
                print("Generated reports:")
                for format_type, filepath in files.items():
                    print(f"  {format_type.upper():8} -> {filepath}")
                print()
            
            print("Analysis complete!")
            
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

