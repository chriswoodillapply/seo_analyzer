#!/usr/bin/env python3
"""
Unit Tests for Lighthouse Individual Results
Tests that Lighthouse returns individual results for each audit instead of summary results.
"""

import pytest
import sys
import os
from typing import List

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator
from src.tests.performance.lighthouse_audit import LighthouseAuditTest
from src.core.test_interface import TestResult, TestStatus, TestSeverity


class TestLighthouseIndividualResults:
    """Test that Lighthouse returns individual results for each audit"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create SEO orchestrator for testing"""
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-Test/1.0',
            timeout=30,
            headless=True,
            enable_javascript=True,
            output_dir='test_lighthouse_results',
            verbose=False,
            enable_caching=True,
            cache_max_age_hours=1,
            save_css=True,
            force_refresh=True
        )
    
    @pytest.fixture
    def lighthouse_test(self):
        """Create Lighthouse test instance"""
        return LighthouseAuditTest()
    
    def test_lighthouse_returns_individual_results(self, orchestrator, lighthouse_test):
        """Test that Lighthouse returns individual results, not summary"""
        # Test URL
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # Fetch content
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            assert content is not None
            assert content.url == test_url
            
            # Run Lighthouse test
            results = lighthouse_test.execute(content, None)
            
            # Verify results are individual, not summary
            assert isinstance(results, list), "Results should be a list of individual results"
            assert len(results) > 0, "Should have at least one result"
            
            # Check that we have individual audit results, not summary
            individual_audits = [r for r in results if r.test_id.startswith('lighthouse_')]
            assert len(individual_audits) > 0, "Should have individual Lighthouse audit results"
            
            # Verify individual results have specific audit IDs
            audit_ids = [r.test_id for r in individual_audits]
            expected_audit_types = ['first-contentful-paint', 'largest-contentful-paint', 'speed-index']
            
            # Should have at least some of the expected audit types
            found_audit_types = [aid for aid in audit_ids if any(expected in aid for expected in expected_audit_types)]
            assert len(found_audit_types) > 0, f"Should have specific audit types, got: {audit_ids}"
    
    def test_lighthouse_results_have_detailed_scores(self, orchestrator, lighthouse_test):
        """Test that individual Lighthouse results have detailed scores"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = lighthouse_test.execute(content, None)
            
            # Check that results have detailed scores
            for result in results:
                if result.test_id.startswith('lighthouse_'):
                    assert result.score is not None, f"Result {result.test_id} should have a score"
                    assert result.score != "13 total audits", f"Result {result.test_id} should not be a summary score"
                    assert '%' in result.score or 'Impact:' in result.score, f"Score should be detailed: {result.score}"
    
    def test_lighthouse_results_have_specific_recommendations(self, orchestrator, lighthouse_test):
        """Test that individual Lighthouse results have specific recommendations"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = lighthouse_test.execute(content, None)
            
            # Check that results have specific recommendations
            for result in results:
                if result.test_id.startswith('lighthouse_'):
                    assert result.recommendation is not None, f"Result {result.test_id} should have a recommendation"
                    assert len(result.recommendation) > 20, f"Recommendation should be detailed: {result.recommendation}"
                    assert "Lighthouse found" not in result.recommendation, f"Should not be summary recommendation: {result.recommendation}"
    
    def test_lighthouse_results_categorization(self, orchestrator, lighthouse_test):
        """Test that individual Lighthouse results are properly categorized"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = lighthouse_test.execute(content, None)
            
            # Check categorization
            categories = set()
            for result in results:
                if result.test_id.startswith('lighthouse_'):
                    assert result.category is not None, f"Result {result.test_id} should have a category"
                    categories.add(result.category)
            
            # Should have multiple categories (Performance, Accessibility, etc.)
            assert len(categories) > 1, f"Should have multiple categories, got: {categories}"
    
    def test_lighthouse_results_severity_levels(self, orchestrator, lighthouse_test):
        """Test that individual Lighthouse results have appropriate severity levels"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = lighthouse_test.execute(content, None)
            
            # Check severity levels
            severities = set()
            for result in results:
                if result.test_id.startswith('lighthouse_'):
                    assert result.severity is not None, f"Result {result.test_id} should have a severity"
                    severities.add(result.severity)
            
            # Should have multiple severity levels
            assert len(severities) > 1, f"Should have multiple severity levels, got: {severities}"
            
            # Should have some critical/high severity issues
            high_severity = [r for r in results if r.severity in [TestSeverity.CRITICAL, TestSeverity.HIGH]]
            assert len(high_severity) > 0, "Should have some high severity issues"
