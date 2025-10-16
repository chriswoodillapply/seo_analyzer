#!/usr/bin/env python3
"""Quick monitor for ongoing analysis"""
import sys
from pathlib import Path
import time

sys.path.insert(0, 'src')

print('Checking analysis progress...\n')

# Check content cache
cache_dir = Path('output/content_cache')
if cache_dir.exists():
    site_dirs = [d for d in cache_dir.iterdir() if d.is_dir()]
    for site_dir in site_dirs:
        url_dirs = [d for d in site_dir.iterdir() if d.is_dir()]
        print(f'Content Cache: {len(url_dirs)} pages cached')
        
        if url_dirs:
            # Find most recent
            most_recent = max(url_dirs, key=lambda d: (d / 'metadata.json').stat().st_mtime if (d / 'metadata.json').exists() else 0)
            if (most_recent / 'metadata.json').exists():
                age = time.time() - (most_recent / 'metadata.json').stat().st_mtime
                print(f'Last cached: {int(age)}s ago')

# Check reports
report_dir = Path('output')
if report_dir.exists():
    xlsx = sorted(report_dir.glob('seo_report_*.xlsx'), key=lambda x: x.stat().st_mtime, reverse=True)
    if xlsx:
        latest = xlsx[0]
        age = time.time() - latest.stat().st_mtime
        size = latest.stat().st_size / (1024 * 1024)
        print(f'\nLatest Report: {latest.name}')
        print(f'Size: {size:.2f} MB, Age: {int(age)}s')

print('\nRun this script again to check progress')


