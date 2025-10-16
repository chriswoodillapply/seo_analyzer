#!/usr/bin/env python3
"""
Check progress of ongoing crawl and analysis
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, 'src')

print('='*80)
print('  CHECKING ANALYSIS PROGRESS')
print('='*80)

# Check if cache directory exists and count cached pages
cache_dir = Path('output/content_cache')
if cache_dir.exists():
    print('\n[Content Cache]')
    
    # Find site directories
    site_dirs = [d for d in cache_dir.iterdir() if d.is_dir()]
    
    for site_dir in site_dirs:
        url_dirs = [d for d in site_dir.iterdir() if d.is_dir()]
        print(f'  Site: {site_dir.name}')
        print(f'  Cached pages: {len(url_dirs)}')
        
        if url_dirs:
            # Show most recent cache
            most_recent = None
            for url_dir in url_dirs:
                metadata_file = url_dir / 'metadata.json'
                if metadata_file.exists():
                    mtime = metadata_file.stat().st_mtime
                    if most_recent is None or mtime > most_recent:
                        most_recent = mtime
            
            if most_recent:
                age_seconds = time.time() - most_recent
                print(f'  Last cached: {int(age_seconds)} seconds ago')
else:
    print('\n[Content Cache]')
    print('  No cache directory found yet')

# Check for reports
report_dir = Path('output')
if report_dir.exists():
    print('\n[Reports]')
    
    csv_files = sorted(report_dir.glob('seo_report_*.csv'), key=lambda x: x.stat().st_mtime, reverse=True)
    excel_files = sorted(report_dir.glob('seo_report_*.xlsx'), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if csv_files:
        latest = csv_files[0]
        age_seconds = time.time() - latest.stat().st_mtime
        size_mb = latest.stat().st_size / (1024 * 1024)
        print(f'  Latest CSV: {latest.name}')
        print(f'  Size: {size_mb:.2f} MB')
        print(f'  Age: {int(age_seconds)} seconds ago')
    
    if excel_files:
        latest = excel_files[0]
        age_seconds = time.time() - latest.stat().st_mtime
        size_mb = latest.stat().st_size / (1024 * 1024)
        print(f'  Latest Excel: {latest.name}')
        print(f'  Size: {size_mb:.2f} MB')
        print(f'  Age: {int(age_seconds)} seconds ago')
    
    if not csv_files and not excel_files:
        print('  No reports generated yet')
else:
    print('\n[Reports]')
    print('  No output directory found yet')

print('\n' + '='*80)
print('  Analysis is running in the background')
print('  Re-run this script to check progress')
print('='*80 + '\n')

