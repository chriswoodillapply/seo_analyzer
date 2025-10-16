#!/usr/bin/env python3
"""
Test SEO Orchestrator with real website analysis
"""

import pytest
import sys
import os
from typing import List, Dict, Any

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator


class TestSEOOrchestrator:
    """Test SEO Orchestrator with real website analysis"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create SEO orchestrator instance for testing"""
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-Test/1.0',
            timeout=30,
            headless=True,
            enable_javascript=True,
            output_dir='test_output',
            verbose=True
        )
    
    def test_single_url_analysis(self, orchestrator):
        """Test analyzing a single URL from applydigital.com"""
        url = "https://www.applydigital.com"
        
        # Analyze single URL
        results = orchestrator.analyze_single_url(url)
        
        # Verify results
        assert isinstance(results, list)
        assert len(results) > 0, "Should have test results"
        
        # Check that we have various test categories
        categories = set(result.category for result in results)
        expected_categories = {
            'Accessibility', 'Content', 'Core Web Vitals', 'Header Structure',
            'Images', 'International SEO', 'Links', 'Meta Tags', 'Mobile Usability',
            'Performance', 'Security', 'Structured Data', 'Technical SEO'
        }
        
        # Should have multiple categories
        assert len(categories) > 5, f"Expected multiple categories, got: {categories}"
        
        # Check result structure
        for result in results[:5]:  # Check first 5 results
            assert hasattr(result, 'url')
            assert hasattr(result, 'test_id')
            assert hasattr(result, 'test_name')
            assert hasattr(result, 'category')
            assert hasattr(result, 'status')
            assert hasattr(result, 'severity')
            assert result.url == url
        
        print(f"\n✅ Single URL Analysis Complete")
        print(f"   URL: {url}")
        print(f"   Tests executed: {len(results)}")
        print(f"   Categories: {len(categories)}")
        
        # Print summary
        status_counts = {}
        for result in results:
            status = result.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"   Results: {status_counts}")
    
    def test_multiple_urls_analysis(self, orchestrator):
        """Test analyzing multiple URLs from applydigital.com"""
        urls = [
            "https://www.applydigital.com",
            "https://www.applydigital.com/about",
            "https://www.applydigital.com/services"
        ]
        
        # Analyze multiple URLs
        summary = orchestrator.analyze_multiple_urls(urls)
        
        # Verify summary structure
        assert isinstance(summary, dict)
        assert 'total_urls' in summary
        assert 'successful' in summary
        assert 'failed' in summary
        assert 'total_tests' in summary
        assert 'analyzed_urls' in summary
        
        # Verify results
        assert summary['total_urls'] == len(urls)
        assert summary['successful'] > 0, "Should have at least one successful analysis"
        assert summary['total_tests'] > 0, "Should have executed tests"
        
        print(f"\n✅ Multiple URLs Analysis Complete")
        print(f"   URLs analyzed: {summary['successful']}/{summary['total_urls']}")
        print(f"   Total tests: {summary['total_tests']}")
    
    def test_crawling_analysis(self, orchestrator):
        """Test crawling and analyzing applydigital.com"""
        start_urls = ["https://www.applydigital.com"]
        
        # Analyze with crawling (limited scope for testing)
        summary = orchestrator.analyze_with_crawling(
            start_urls=start_urls,
            max_depth=1,  # Shallow crawl for testing
            max_urls=10,   # Limit URLs for testing
            test_ids=None  # Run all tests
        )
        
        # Verify summary structure
        assert isinstance(summary, dict)
        assert 'total_urls' in summary
        assert 'successful' in summary
        assert 'crawl_stats' in summary
        
        # Verify crawl stats
        crawl_stats = summary['crawl_stats']
        assert isinstance(crawl_stats, dict)
        assert 'total_urls' in crawl_stats
        assert 'visited_urls' in crawl_stats
        
        print(f"\n✅ Crawling Analysis Complete")
        print(f"   URLs discovered: {crawl_stats.get('total_urls', 0)}")
        print(f"   URLs analyzed: {summary['successful']}")
        print(f"   Total tests: {summary['total_tests']}")
    
    def test_report_generation(self, orchestrator):
        """Test report generation after analysis"""
        # First analyze a URL
        url = "https://www.applydigital.com"
        orchestrator.analyze_single_url(url)
        
        # Generate reports
        report_files = orchestrator.generate_reports(
            formats=['json', 'csv'],
            base_filename='test_applydigital_analysis'
        )
        
        # Verify reports were generated
        assert isinstance(report_files, dict)
        assert len(report_files) > 0, "Should have generated at least one report"
        
        # Check specific formats
        if 'json' in report_files:
            json_file = report_files['json']
            assert os.path.exists(json_file), f"JSON report should exist: {json_file}"
        
        if 'csv' in report_files:
            csv_file = report_files['csv']
            assert os.path.exists(csv_file), f"CSV report should exist: {csv_file}"
        
        print(f"\n✅ Report Generation Complete")
        print(f"   Generated reports: {list(report_files.keys())}")
        for format_type, file_path in report_files.items():
            print(f"   {format_type.upper()}: {file_path}")
    
    def test_summary_statistics(self, orchestrator):
        """Test summary statistics functionality"""
        # Analyze a URL first
        url = "https://www.applydigital.com"
        orchestrator.analyze_single_url(url)
        
        # Get summary stats
        stats = orchestrator.get_summary_stats()
        
        # Verify stats structure
        assert isinstance(stats, dict)
        assert 'total_tests' in stats
        assert 'passed' in stats
        assert 'failed' in stats
        assert 'warnings' in stats
        assert 'pass_rate' in stats
        assert 'urls_analyzed' in stats
        assert 'categories' in stats
        
        # Verify values
        assert stats['total_tests'] > 0
        assert stats['urls_analyzed'] > 0
        assert 0 <= stats['pass_rate'] <= 100
        
        # Print summary
        orchestrator.print_summary()
        
        print(f"\n✅ Summary Statistics Complete")
        print(f"   Total tests: {stats['total_tests']}")
        print(f"   Pass rate: {stats['pass_rate']:.1f}%")
        print(f"   Categories: {len(stats['categories'])}")
    
    def test_results_filtering(self, orchestrator):
        """Test result filtering by various criteria"""
        # Analyze a URL first
        url = "https://www.applydigital.com"
        orchestrator.analyze_single_url(url)
        
        # Test filtering by URL
        url_results = orchestrator.get_results_by_url(url)
        assert len(url_results) > 0, "Should have results for the analyzed URL"
        
        # Test filtering by status
        all_results = orchestrator.get_results()
        statuses = set(result.get('Status') for result in all_results)
        
        for status in statuses:
            status_results = orchestrator.get_results_by_status(status)
            assert len(status_results) > 0, f"Should have results with status {status}"
        
        # Test filtering by category
        categories = set(result.get('Category') for result in all_results)
        
        for category in categories:
            category_results = orchestrator.get_results_by_category(category)
            assert len(category_results) > 0, f"Should have results for category {category}"
        
        print(f"\n✅ Result Filtering Complete")
        print(f"   Total results: {len(all_results)}")
        print(f"   Statuses: {statuses}")
        print(f"   Categories: {categories}")
    
    def test_orchestrator_cleanup(self, orchestrator):
        """Test that orchestrator properly cleans up resources"""
        # Use context manager to ensure cleanup
        with SEOOrchestrator(
            user_agent='SEO-Analyzer-Test/1.0',
            timeout=30,
            headless=True,
            enable_javascript=True,
            output_dir='test_output',
            verbose=False
        ) as test_orchestrator:
            
            # Analyze a URL
            url = "https://www.applydigital.com"
            results = test_orchestrator.analyze_single_url(url)
            
            # Verify analysis worked
            assert len(results) > 0
        
        # Context manager should have cleaned up
        print(f"\n✅ Orchestrator Cleanup Complete")


if __name__ == "__main__":
    # Run the test directly
    pytest.main([__file__, "-v", "-s"])
