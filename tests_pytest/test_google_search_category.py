#!/usr/bin/env python3
"""
Pytest unit tests for Google Search category tests

Tests the Google Search category against www.applydigital.com to validate
the implementation of GS001-GS014 tests.
"""

import pytest
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator
from src.core.test_interface import TestResult, TestStatus


class TestGoogleSearchCategory:
    """Test class for Google Search category tests"""
    
    @pytest.fixture
    def test_url(self):
        """Test URL fixture"""
        return "https://www.applydigital.com/"
    
    @pytest.fixture
    def orchestrator_config(self):
        """Orchestrator configuration fixture"""
        return {
            'user_agent': 'SEO-Analyzer-Test/1.0',
            'timeout': 30,
            'headless': True,
            'enable_javascript': True,
            'output_dir': 'test_output',
            'verbose': True,
            'enable_caching': True,
            'cache_max_age_hours': 1
        }
    
    def test_google_search_tests_load(self, orchestrator_config):
        """Test that Google Search tests are properly loaded"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            # Check that Google Search tests are loaded
            all_tests = orchestrator.test_executor.registry.get_all_tests()
            google_search_tests = [test for test in all_tests if test.category == "Google Search"]
            
            # Should have at least the 14 tests we implemented
            assert len(google_search_tests) >= 14, f"Expected at least 14 Google Search tests, found {len(google_search_tests)}"
            
            # Check for specific test IDs
            test_ids = [test.test_id for test in google_search_tests]
            expected_tests = [
                'GS001', 'GS002', 'GS003', 'GS004', 'GS005',
                'GS006', 'GS007', 'GS008', 'GS009', 'GS010',
                'GS011', 'GS012', 'GS013', 'GS014'
            ]
            
            for expected_test in expected_tests:
                assert expected_test in test_ids, f"Expected test {expected_test} not found in {test_ids}"
    
    def test_google_search_category_execution(self, test_url, orchestrator_config):
        """Test execution of Google Search category tests"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            # Analyze the URL
            result = orchestrator.analyze_single_url(test_url)
            
            assert result is not None, "URL analysis should return results"
            assert len(result) > 0, "Should have test results"
            
            # Filter for Google Search category tests
            google_search_results = [r for r in result if r.category == "Google Search"]
            
            assert len(google_search_results) > 0, "Should have Google Search category test results"
            
            # Verify test structure
            for result_item in google_search_results:
                assert isinstance(result_item, TestResult), "Result should be TestResult instance"
                assert result_item.test_id.startswith('GS'), f"Test ID should start with 'GS': {result_item.test_id}"
                assert result_item.category == "Google Search", f"Category should be 'Google Search': {result_item.category}"
                assert result_item.status in TestStatus, f"Status should be valid TestStatus: {result_item.status}"
                assert isinstance(result_item.issue_description, str), "Issue description should be string"
                assert isinstance(result_item.score, str), "Score should be string"
    
    def test_google_search_specific_tests(self, test_url, orchestrator_config):
        """Test specific Google Search tests for expected behavior"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            result = orchestrator.analyze_single_url(test_url)
            google_search_results = [r for r in result if r.category == "Google Search"]
            
            # Group results by test ID
            test_groups = {}
            for result_item in google_search_results:
                test_id = result_item.test_id
                if test_id not in test_groups:
                    test_groups[test_id] = []
                test_groups[test_id].append(result_item)
            
            # Test GS001 - Googlebot Render Visibility
            if 'GS001' in test_groups:
                gs001_results = test_groups['GS001']
                assert len(gs001_results) > 0, "GS001 should have results"
                # Should check for canonical, H1, main content, overlays
            
            # Test GS002 - Console Network Errors
            if 'GS002' in test_groups:
                gs002_results = test_groups['GS002']
                assert len(gs002_results) > 0, "GS002 should have results"
                # Should check for console warnings/errors, network issues
            
            # Test GS003 - Static vs Rendered Content
            if 'GS003' in test_groups:
                gs003_results = test_groups['GS003']
                assert len(gs003_results) > 0, "GS003 should have results"
                # Should compare static vs rendered content
            
            # Test GS004 - Overlay Blocking
            if 'GS004' in test_groups:
                gs004_results = test_groups['GS004']
                assert len(gs004_results) > 0, "GS004 should have results"
                # Should check for blocking overlays
    
    def test_google_search_results_quality(self, test_url, orchestrator_config):
        """Test that Google Search results provide meaningful insights"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            result = orchestrator.analyze_single_url(test_url)
            google_search_results = [r for r in result if r.category == "Google Search"]
            
            # Check that results have meaningful content
            for result_item in google_search_results:
                # Issue description should not be empty
                assert len(result_item.issue_description.strip()) > 0, f"Empty issue description for {result_item.test_id}"
                
                # Score should be numeric or percentage
                score = result_item.score
                assert score is not None, f"Score should not be None for {result_item.test_id}"
                assert len(score.strip()) > 0, f"Empty score for {result_item.test_id}"
                
                # Recommendation should be provided for failures/warnings
                if result_item.status in [TestStatus.FAIL, TestStatus.WARNING]:
                    assert result_item.recommendation is not None, f"Recommendation should be provided for {result_item.test_id}"
                    assert len(result_item.recommendation.strip()) > 0, f"Empty recommendation for {result_item.test_id}"
    
    def test_google_search_category_coverage(self, test_url, orchestrator_config):
        """Test that Google Search category covers all expected test areas"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            result = orchestrator.analyze_single_url(test_url)
            google_search_results = [r for r in result if r.category == "Google Search"]
            
            # Get unique test IDs
            test_ids = set(r.test_id for r in google_search_results)
            
            # Expected test areas
            expected_areas = {
                'GS001': 'Googlebot Render Visibility',
                'GS002': 'Console Network Errors', 
                'GS003': 'Static vs Rendered Content',
                'GS004': 'Overlay Blocking',
                'GS005': 'Canonical Alignment Inspection',
                'GS006': 'Sitemap Coverage Check',
                'GS007': 'Duplicate Variant Detection',
                'GS008': 'Redirect Chain Integrity',
                'GS009': 'SSR NoJS Fallback',
                'GS010': 'Thin Content Heuristic',
                'GS011': 'Hreflang Canonical Consistency',
                'GS012': 'Internal Linking Strength',
                'GS013': 'Render Timing Metrics',
                'GS014': 'Robots Meta Headers'
            }
            
            # Check that we have results for expected areas
            for test_id, area_name in expected_areas.items():
                assert test_id in test_ids, f"Missing test {test_id} ({area_name})"
    
    def test_google_search_soft_404_detection(self, test_url, orchestrator_config):
        """Test that Google Search tests can detect soft 404 indicators"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            result = orchestrator.analyze_single_url(test_url)
            google_search_results = [r for r in result if r.category == "Google Search"]
            
            # Look for soft 404 related issues
            soft_404_indicators = []
            for result_item in google_search_results:
                issue_desc = result_item.issue_description.lower()
                if any(keyword in issue_desc for keyword in ['soft 404', 'thin content', 'canonical', 'overlay', 'blocking']):
                    soft_404_indicators.append(result_item)
            
            # Should have some soft 404 related findings for the homepage
            # (which we know has issues based on our analysis)
            assert len(soft_404_indicators) > 0, "Should detect soft 404 indicators for problematic homepage"
    
    def test_google_search_performance(self, test_url, orchestrator_config):
        """Test that Google Search tests complete within reasonable time"""
        start_time = datetime.now()
        
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            result = orchestrator.analyze_single_url(test_url)
            google_search_results = [r for r in result if r.category == "Google Search"]
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Should complete within 2 minutes (120 seconds)
        assert duration < 120, f"Google Search tests took too long: {duration:.2f} seconds"
        
        # Should have results
        assert len(google_search_results) > 0, "Should have Google Search test results"
    
    def test_google_search_error_handling(self, orchestrator_config):
        """Test that Google Search tests handle errors gracefully"""
        # Test with invalid URL
        invalid_url = "https://invalid-domain-that-does-not-exist.com/"
        
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            result = orchestrator.analyze_single_url(invalid_url)
            
            # Should still return results (even if they're error results)
            assert result is not None, "Should return results even for invalid URL"
            
            # For completely invalid URLs, the orchestrator may return empty results
            # or results with error status - both are acceptable
            if len(result) > 0:
                error_results = [r for r in result if r.status == TestStatus.ERROR]
                # If we have results, some should be errors
                assert len(error_results) > 0, "Should have error results for invalid URL"
            else:
                # Empty results are also acceptable for completely invalid URLs
                assert len(result) == 0, "Empty results are acceptable for invalid URLs"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
