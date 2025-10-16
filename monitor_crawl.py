#!/usr/bin/env python3
"""Monitor the crawl progress"""

import os
import glob
import time

print("\n" + "="*80)
print("  MONITORING SITE-WIDE CRAWL PROGRESS")
print("="*80)
print("\nCrawl Configuration:")
print("  Target: https://www.applydigital.com")
print("  Max Depth: 5 levels")
print("  Max URLs: 1,000")
print("  Tests per URL: 93")
print("  Expected Duration: 15-30 minutes")
print("\nThis will analyze:")
print("  - All discoverable pages on the site")
print("  - Meta tags, headers, images, links")
print("  - Performance, accessibility, security")
print("  - Mobile usability, structured data")
print("  - And 80+ more SEO factors")

print("\n" + "-"*80)
print("Crawl is running in the background...")
print("Checking for output files...")
print("-"*80)

# Look for the most recent output files
output_dir = "output"
if os.path.exists(output_dir):
    # Find discovered URLs files
    discovered_files = sorted(glob.glob(f"{output_dir}/discovered_urls_*.txt"), reverse=True)
    
    # Find analysis files
    csv_files = sorted(glob.glob(f"{output_dir}/*_analysis_*.csv"), reverse=True)
    excel_files = sorted(glob.glob(f"{output_dir}/*_analysis_*.xlsx"), reverse=True)
    
    if discovered_files:
        print(f"\nDiscovered URLs file: {discovered_files[0]}")
        try:
            with open(discovered_files[0], 'r') as f:
                urls = f.readlines()
                print(f"  URLs found so far: {len(urls)}")
        except:
            print("  (Still being written...)")
    
    if csv_files:
        print(f"\nAnalysis in progress: {csv_files[0]}")
    elif excel_files:
        print(f"\nAnalysis in progress: {excel_files[0]}")
    else:
        print("\nCrawl phase in progress - URL discovery underway...")
        print("Analysis will begin after crawling completes.")

print("\n" + "="*80)
print("WHAT'S HAPPENING:")
print("="*80)
print("""
Phase 1: URL Discovery (5-10 min)
  - Starting from homepage
  - Following all internal links
  - Building sitemap up to depth 5
  - Limiting to 1,000 URLs

Phase 2: Content Fetching (10-20 min)
  - Fetching static HTML for each page
  - Rendering JavaScript content
  - Measuring load times
  - Capturing Core Web Vitals

Phase 3: SEO Analysis (5-10 min)
  - Running 93 tests per page
  - Checking meta tags, headers, images
  - Analyzing performance, accessibility
  - Validating structured data

Phase 4: Report Generation (1-2 min)
  - Consolidating all results
  - Generating Excel report
  - Creating summary statistics
  - Identifying patterns across site
""")

print("\n" + "="*80)
print("TO CHECK PROGRESS:")
print("="*80)
print("  Run this script again: python monitor_crawl.py")
print("  Watch for files in: output/")
print("  Look for: multi_url_analysis_*.xlsx")
print("\n" + "="*80 + "\n")

