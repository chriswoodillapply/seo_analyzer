#!/usr/bin/env python3
"""
Fixed Full SEO Analysis Test for ApplyDigital.com
"""

import sys
import os
from datetime import datetime

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, 'seo_analyzer')

from src.core.seo_orchestrator import SEOOrchestrator

def main():
    print("\n" + "="*80)
    print("🚀 FULL SEO ANALYSIS: ApplyDigital.com (FIXED)")
    print("="*80)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🌐 Target: https://www.applydigital.com")
    print("📊 Max URLs: 1000")
    print("🔍 Max Depth: 10 levels")
    print("📋 Output: Excel format")
    print("="*80)
    
    # Create output directory first
    output_dir = 'full_analysis_output'
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Created output directory: {output_dir}")
    
    # Create orchestrator
    orchestrator = SEOOrchestrator(
        user_agent='SEO-Analyzer-Full/1.0',
        timeout=60,
        headless=True,
        enable_javascript=True,
        output_dir=output_dir,
        verbose=True
    )
    
    try:
        start_urls = ["https://www.applydigital.com"]
        
        # Run comprehensive crawling and analysis
        print("\n🔍 Starting URL Discovery...")
        summary = orchestrator.analyze_with_crawling(
            start_urls=start_urls,
            max_depth=10,      # Deep crawl
            max_urls=1000,     # Comprehensive URL discovery
            test_ids=None       # Run all SEO tests
        )
        
        # Print comprehensive results
        print("\n" + "="*80)
        print("📈 ANALYSIS RESULTS")
        print("="*80)
        
        # Basic stats
        print(f"🌐 URLs Discovered: {summary.get('crawl_stats', {}).get('total_urls', 0)}")
        print(f"✅ URLs Successfully Analyzed: {summary['successful']}")
        print(f"❌ URLs Failed: {summary['failed']}")
        print(f"🧪 Total Tests Executed: {summary['total_tests']}")
        
        # Generate comprehensive reports
        print(f"\n📋 Generating Reports...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"applydigital_full_analysis_{timestamp}"
        
        report_files = orchestrator.generate_reports(
            formats=['excel', 'csv', 'json', 'html'],
            base_filename=base_filename
        )
        
        print(f"\n📁 Generated Reports:")
        for format_type, file_path in report_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   {format_type.upper()}: {file_path} ({file_size:,} bytes)")
            else:
                print(f"   {format_type.upper()}: {file_path} (FILE NOT FOUND)")
        
        # Print detailed summary
        orchestrator.print_summary()
        
        print(f"\n" + "="*80)
        print(f"✅ FULL ANALYSIS COMPLETE")
        print(f"📅 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Reports saved to: {output_dir}/")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        return False
        
    finally:
        orchestrator.cleanup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
