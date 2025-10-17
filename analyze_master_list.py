#!/usr/bin/env python3
"""
Comprehensive SEO Analysis of Master URL List
- Detailed logging to track time spent in each phase
- Batch processing for better performance
- All available tests including Lighthouse and Axe-core
"""

import sys
import os
import time
from datetime import datetime
from urllib.parse import urljoin

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, '.')

from src.core.seo_orchestrator import SEOOrchestrator

def log_with_timestamp(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] {message}')

def analyze_urls_in_batches(urls, batch_size=50, max_batches=None):
    """Analyze URLs in batches with detailed logging"""
    
    log_with_timestamp('🚀 COMPREHENSIVE SEO ANALYSIS - MASTER URL LIST')
    print('='*80)
    log_with_timestamp(f'📅 Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    log_with_timestamp(f'🌐 Total URLs: {len(urls)}')
    log_with_timestamp(f'📦 Batch size: {batch_size}')
    log_with_timestamp(f'🧪 Tests: ALL available tests (Lighthouse + Axe-core + all SEO tests)')
    print('='*80)
    
    # Initialize orchestrator
    log_with_timestamp('🔧 Initializing SEO Orchestrator...')
    start_time = time.time()
    
    with SEOOrchestrator(
        user_agent='SEO-Analyzer-Master-List/1.0',
        timeout=60,
        headless=True,
        enable_javascript=True,
        output_dir='master_list_analysis',
        verbose=True,
        enable_caching=True,
        cache_max_age_hours=24,
        save_css=True,
        force_refresh=True
    ) as orch:
        init_time = time.time() - start_time
        log_with_timestamp(f'✅ Orchestrator initialized in {init_time:.2f}s')
        
        # Process URLs in batches
        total_analyzed = 0
        total_failed = 0
        all_results = []
        
        # Calculate batches
        num_batches = min(len(urls) // batch_size + (1 if len(urls) % batch_size else 0), 
                         max_batches or len(urls) // batch_size + 1)
        
        log_with_timestamp(f'📦 Processing {len(urls)} URLs in {num_batches} batches of {batch_size}')
        
        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(urls))
            batch_urls = urls[start_idx:end_idx]
            
            log_with_timestamp(f'\\n📦 BATCH {batch_num + 1}/{num_batches}')
            log_with_timestamp(f'   URLs {start_idx + 1}-{end_idx} of {len(urls)}')
            log_with_timestamp(f'   Sample URLs: {batch_urls[:3]}...')
            
            # Analyze this batch
            batch_start = time.time()
            log_with_timestamp('   🔍 Starting batch analysis...')
            
            try:
                summary = orch.analyze_multiple_urls(batch_urls)
                batch_time = time.time() - batch_start
                
                log_with_timestamp(f'   ✅ Batch completed in {batch_time:.2f}s')
                log_with_timestamp(f'   📊 Batch results: {summary["successful"]} successful, {summary["failed"]} failed')
                log_with_timestamp(f'   🧪 Tests executed: {summary["total_tests"]}')
                
                # Accumulate results
                total_analyzed += summary["successful"]
                total_failed += summary["failed"]
                
                # Get results for this batch
                batch_results = orch.test_executor.get_results()
                all_results.extend(batch_results)
                
                # Show progress
                progress = ((batch_num + 1) / num_batches) * 100
                log_with_timestamp(f'   📈 Overall progress: {progress:.1f}% ({total_analyzed + total_failed}/{len(urls)} URLs)')
                
            except Exception as e:
                log_with_timestamp(f'   ❌ Batch failed: {e}')
                continue
        
        # Final analysis
        log_with_timestamp(f'\\n📈 FINAL ANALYSIS RESULTS')
        print('='*80)
        log_with_timestamp(f'✅ Total URLs Analyzed: {total_analyzed}')
        log_with_timestamp(f'❌ Total URLs Failed: {total_failed}')
        log_with_timestamp(f'🧪 Total Tests Executed: {len(all_results)}')
        log_with_timestamp(f'📊 Success Rate: {(total_analyzed / (total_analyzed + total_failed) * 100):.1f}%')
        
        # Analyze results by category
        categories = {}
        for result in all_results:
            cat = result.category
            categories[cat] = categories.get(cat, 0) + 1
        
        log_with_timestamp(f'\\n📋 Results by Category:')
        for cat, count in sorted(categories.items()):
            log_with_timestamp(f'  {cat}: {count} results')
        
        # Check for multi-result tests
        lighthouse_results = [r for r in all_results if 'lighthouse' in r.test_id]
        axe_results = [r for r in all_results if 'axe' in r.test_id]
        
        log_with_timestamp(f'\\n🔍 Multi-Result Tests:')
        log_with_timestamp(f'  Lighthouse results: {len(lighthouse_results)}')
        log_with_timestamp(f'  Axe-core results: {len(axe_results)}')
        
        # Generate comprehensive reports
        log_with_timestamp(f'\\n📋 Generating Reports...')
        report_start = time.time()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f'seo_master_list_{timestamp}'
        
        report_files = orch.generate_reports(
            formats=['excel', 'csv', 'json', 'html'],
            base_filename=base_filename
        )
        
        report_time = time.time() - report_start
        log_with_timestamp(f'✅ Reports generated in {report_time:.2f}s')
        
        log_with_timestamp(f'\\n📁 Generated Reports:')
        log_with_timestamp(f'📝 Base filename: {base_filename}')
        for format_type, file_path in report_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                log_with_timestamp(f'   {format_type.upper()}: {file_path} ({file_size:,} bytes)')
        
        # Show sample results
        if lighthouse_results:
            log_with_timestamp(f'\\n📋 Sample Lighthouse Results:')
            for i, result in enumerate(lighthouse_results[:3]):
                log_with_timestamp(f'  {i+1}. {result.test_name}: {result.status.value}')
                log_with_timestamp(f'      Issue: {result.issue_description[:60]}...')
        
        if axe_results:
            log_with_timestamp(f'\\n📋 Sample Axe-core Results:')
            for i, result in enumerate(axe_results[:3]):
                log_with_timestamp(f'  {i+1}. {result.test_name}: {result.status.value}')
                log_with_timestamp(f'      Issue: {result.issue_description[:60]}...')
    
    total_time = time.time() - start_time
    log_with_timestamp(f'\\n✅ MASTER LIST ANALYSIS COMPLETE!')
    log_with_timestamp(f'📅 Finished at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    log_with_timestamp(f'⏱️  Total time: {total_time:.2f}s ({total_time/60:.1f} minutes)')
    log_with_timestamp(f'📁 Reports saved to: master_list_analysis/')
    print('='*80)

def main():
    """Main function to run the analysis"""
    
    # Read URLs from master list
    log_with_timestamp('📋 Loading URLs from master list...')
    with open('../applydigitalurls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Convert to full URLs
    full_urls = []
    for url in urls:
        if not url.startswith('http'):
            full_urls.append(f'https://{url}')
        else:
            full_urls.append(url)
    
    log_with_timestamp(f'📋 Loaded {len(full_urls)} URLs from master list')
    
    # Start with a smaller batch for testing
    test_batch_size = 100  # Start with 20 URLs
    max_test_batches = 5  # Only process 1 batch initially
    
    log_with_timestamp(f'🧪 TESTING MODE: Processing {test_batch_size} URLs in {max_test_batches} batch')
    log_with_timestamp('   (This is a test run - increase batch_size and max_batches for full analysis)')
    
    # Run analysis
    analyze_urls_in_batches(full_urls, batch_size=test_batch_size, max_batches=max_test_batches)

if __name__ == "__main__":
    main()
