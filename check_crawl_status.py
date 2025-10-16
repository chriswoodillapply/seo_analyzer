#!/usr/bin/env python3
"""Real-time crawl status checker"""

import os
import glob
import time
from datetime import datetime

def check_status():
    print("\n" + "="*80)
    print(f"  CRAWL STATUS CHECK - {datetime.now().strftime('%I:%M:%S %p')}")
    print("="*80)
    
    # Check for output files
    output_dir = "output"
    
    # Look for discovered URLs
    discovered_files = sorted(glob.glob(f"{output_dir}/discovered_urls_*.txt"), reverse=True)
    
    # Look for analysis files
    analysis_csv = sorted(glob.glob(f"{output_dir}/multi_url_analysis_*.csv"), reverse=True)
    analysis_xlsx = sorted(glob.glob(f"{output_dir}/multi_url_analysis_*.xlsx"), reverse=True)
    
    print("\nPROGRESS:")
    print("-"*80)
    
    if not discovered_files:
        print("Phase: URL DISCOVERY (Just started)")
        print("  [*] Crawling www.applydigital.com...")
        print("  [*] Following internal links...")
        print("  [*] Building sitemap...")
        print("\n  Status: URLs are being discovered (file will appear soon)")
        
    elif discovered_files:
        latest_discovered = discovered_files[0]
        print(f"Phase: URL DISCOVERY (In progress)")
        print(f"  File: {os.path.basename(latest_discovered)}")
        
        try:
            with open(latest_discovered, 'r') as f:
                urls = f.readlines()
                url_count = len(urls)
                print(f"  [OK] URLs discovered so far: {url_count}")
                
                if url_count > 0:
                    print(f"\n  Sample URLs found:")
                    for url in urls[:5]:
                        print(f"    - {url.strip()}")
                    if url_count > 5:
                        print(f"    ... and {url_count - 5} more")
        except Exception as e:
            print(f"  [WAIT] File is being written...")
    
    if analysis_csv or analysis_xlsx:
        print(f"\nPhase: ANALYSIS (Running)")
        if analysis_csv:
            print(f"  Analysis file: {os.path.basename(analysis_csv[0])}")
        if analysis_xlsx:
            print(f"  Excel report: {os.path.basename(analysis_xlsx[0])}")
        print("  [OK] SEO tests are being executed...")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("-"*80)
    print("  - Wait 5-10 minutes for crawl to complete")
    print("  - Run this script again: python check_crawl_status.py")
    print("  - Final report will be: multi_url_analysis_*.xlsx")
    print("="*80 + "\n")

if __name__ == "__main__":
    check_status()

