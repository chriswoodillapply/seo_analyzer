#!/usr/bin/env python3
"""
Full SEO Analysis of ApplyDigital.com
- Crawl up to 1000 URLs
- Max depth of 10 levels
- Output to Excel format
"""

import pytest
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator


class TestFullApplyDigitalAnalysis:
    """Full SEO analysis of ApplyDigital.com with comprehensive crawling"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create SEO orchestrator instance for full analysis"""
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-Full/1.0',
            timeout=60,  # Longer timeout for comprehensive analysis
            headless=True,
            enable_javascript=True,
            output_dir='full_analysis_output',
            verbose=True
        )
    
    def test_full_applydigital_analysis(self, orchestrator):
        """Run comprehensive SEO analysis of ApplyDigital.com"""
        print("\n" + "="*80)
        print("🚀 FULL SEO ANALYSIS: ApplyDigital.com")
        print("="*80)
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 Target: https://www.applydigital.com")
        print("📊 Max URLs: 1000")
        print("🔍 Max Depth: 10 levels")
        print("📋 Output: Excel format")
        print("="*80)
        
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
        
        # Crawl depth breakdown
        crawl_stats = summary.get('crawl_stats', {})
        if 'by_depth' in crawl_stats:
            print(f"\n📊 URLs by Crawl Depth:")
            for depth, count in crawl_stats['by_depth'].items():
                print(f"   Depth {depth}: {count} URLs")
        
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
        
        # Print detailed summary
        orchestrator.print_summary()
        
        # Get detailed statistics
        stats = orchestrator.get_summary_stats()
        
        print(f"\n📊 DETAILED STATISTICS")
        print("="*80)
        print(f"🎯 Overall Pass Rate: {stats['pass_rate']:.1f}%")
        print(f"📈 Total Tests: {stats['total_tests']}")
        print(f"✅ Passed: {stats['passed']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"⚠️  Warnings: {stats['warnings']}")
        
        # Category breakdown
        print(f"\n📋 Results by Category:")
        print("-" * 80)
        for category, cat_stats in stats['categories'].items():
            pass_rate = (cat_stats['passed'] / cat_stats['total'] * 100) if cat_stats['total'] > 0 else 0
            print(f"{category:20} | Total: {cat_stats['total']:3} | "
                  f"Pass: {cat_stats['passed']:3} | "
                  f"Fail: {cat_stats['failed']:3} | "
                  f"Warn: {cat_stats['warnings']:3} | "
                  f"Rate: {pass_rate:5.1f}%")
        
        # Top issues analysis
        print(f"\n🔍 TOP ISSUES ANALYSIS")
        print("-" * 80)
        
        # Get failed tests
        failed_results = orchestrator.get_results_by_status('Fail')
        if failed_results:
            print(f"❌ Critical Issues ({len(failed_results)}):")
            for i, result in enumerate(failed_results[:10], 1):  # Top 10
                print(f"   {i:2}. {result.get('Test Name', 'Unknown')} - {result.get('URL', 'Unknown')}")
        
        # Get warning tests
        warning_results = orchestrator.get_results_by_status('Warning')
        if warning_results:
            print(f"\n⚠️  Warnings ({len(warning_results)}):")
            for i, result in enumerate(warning_results[:10], 1):  # Top 10
                print(f"   {i:2}. {result.get('Test Name', 'Unknown')} - {result.get('URL', 'Unknown')}")
        
        # Performance insights
        print(f"\n⚡ PERFORMANCE INSIGHTS")
        print("-" * 80)
        
        # Analyze by URL performance
        analyzed_urls = orchestrator.analyzed_urls
        print(f"🌐 URLs Analyzed: {len(analyzed_urls)}")
        
        # Get results by URL to analyze performance
        url_performance = {}
        for url in analyzed_urls[:10]:  # Analyze first 10 URLs
            url_results = orchestrator.get_results_by_url(url)
            if url_results:
                passed = len([r for r in url_results if r.get('Status') == 'Pass'])
                total = len(url_results)
                pass_rate = (passed / total * 100) if total > 0 else 0
                url_performance[url] = {
                    'total_tests': total,
                    'passed': passed,
                    'pass_rate': pass_rate
                }
        
        if url_performance:
            print(f"\n📊 Top URLs Performance:")
            sorted_urls = sorted(url_performance.items(), key=lambda x: x[1]['pass_rate'], reverse=True)
            for url, perf in sorted_urls[:5]:
                print(f"   {perf['pass_rate']:5.1f}% - {url} ({perf['passed']}/{perf['total_tests']} tests)")
        
        print(f"\n" + "="*80)
        print(f"✅ FULL ANALYSIS COMPLETE")
        print(f"📅 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Reports saved to: full_analysis_output/")
        print("="*80)
        
        # Assertions to verify the analysis was successful
        assert summary['successful'] > 0, "Should have successfully analyzed at least one URL"
        assert summary['total_tests'] > 0, "Should have executed tests"
        assert 'excel' in report_files, "Should have generated Excel report"
        assert os.path.exists(report_files['excel']), "Excel report file should exist"
        
        # Verify we have comprehensive data
        assert len(orchestrator.analyzed_urls) > 0, "Should have analyzed URLs"
        assert stats['total_tests'] > 0, "Should have test results"
        
        return {
            'summary': summary,
            'stats': stats,
            'report_files': report_files,
            'analyzed_urls': len(orchestrator.analyzed_urls)
        }


if __name__ == "__main__":
    # Run the test directly
    pytest.main([__file__, "-v", "-s", "--tb=short"])

