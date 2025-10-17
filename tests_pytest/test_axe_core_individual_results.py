#!/usr/bin/env python3
"""
Unit Tests for Axe-core Individual Results
Tests that Axe-core returns individual results for each violation instead of summary results.
"""

import pytest
import sys
import os
from typing import List

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator
from src.tests.accessibility.axe_core_audit import AxeCoreAuditTest
from src.core.test_interface import TestResult, TestStatus, TestSeverity


class TestAxeCoreIndividualResults:
    """Test that Axe-core returns individual results for each violation"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create SEO orchestrator for testing"""
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-Test/1.0',
            timeout=30,
            headless=True,
            enable_javascript=True,
            output_dir='output/test_axe_core_results',
            verbose=False,
            enable_caching=True,
            cache_max_age_hours=1,
            save_css=True,
            force_refresh=True
        )
    
    @pytest.fixture
    def axe_core_test(self):
        """Create Axe-core test instance"""
        return AxeCoreAuditTest()
    
    def test_axe_core_returns_individual_results(self, orchestrator, axe_core_test):
        """Test that Axe-core returns individual results, not summary"""
        # Test URL
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # Fetch content
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            assert content is not None
            assert content.url == test_url
            
            # Run Axe-core test
            results = axe_core_test.execute(content, None)
            
            # Verify results are individual, not summary
            assert isinstance(results, list), "Results should be a list of individual results"
            assert len(results) > 0, "Should have at least one result"
            
            # Check that we have individual violation results, not summary
            individual_violations = [r for r in results if r.test_id.startswith('axe_')]
            assert len(individual_violations) > 0, "Should have individual Axe-core violation results"
            
            # Verify individual results have specific violation IDs
            violation_ids = [r.test_id for r in individual_violations]
            expected_violation_types = ['heading-order', 'color-contrast', 'aria-labels']
            
            # Should have at least some of the expected violation types
            found_violation_types = [vid for vid in violation_ids if any(expected in vid for expected in expected_violation_types)]
            assert len(found_violation_types) > 0, f"Should have specific violation types, got: {violation_ids}"
    
    def test_axe_core_results_have_detailed_scores(self, orchestrator, axe_core_test):
        """Test that individual Axe-core results have detailed scores"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = axe_core_test.execute(content, None)
            
            # Check that results have detailed scores
            for result in results:
                if result.test_id.startswith('axe_'):
                    assert result.score is not None, f"Result {result.test_id} should have a score"
                    assert result.score != "2 total issues", f"Result {result.test_id} should not be a summary score"
                    assert 'Impact:' in result.score, f"Score should be detailed: {result.score}"
    
    def test_axe_core_results_have_specific_recommendations(self, orchestrator, axe_core_test):
        """Test that individual Axe-core results have specific recommendations"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = axe_core_test.execute(content, None)
            
            # Check that results have specific recommendations
            for result in results:
                if result.test_id.startswith('axe_'):
                    assert result.recommendation is not None, f"Result {result.test_id} should have a recommendation"
                    assert len(result.recommendation) > 20, f"Recommendation should be detailed: {result.recommendation}"
                    assert "Axe-core found" not in result.recommendation, f"Should not be summary recommendation: {result.recommendation}"
    
    def test_axe_core_results_accessibility_category(self, orchestrator, axe_core_test):
        """Test that individual Axe-core results are properly categorized as Accessibility"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = axe_core_test.execute(content, None)
            
            # Check categorization
            for result in results:
                if result.test_id.startswith('axe_'):
                    assert result.category == 'Accessibility', f"Result {result.test_id} should be categorized as Accessibility"
    
    def test_axe_core_results_severity_levels(self, orchestrator, axe_core_test):
        """Test that individual Axe-core results have appropriate severity levels"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            content = orchestrator.content_fetcher.fetch_complete(test_url)
            results = axe_core_test.execute(content, None)
            
            # Check severity levels
            severities = set()
            for result in results:
                if result.test_id.startswith('axe_'):
                    assert result.severity is not None, f"Result {result.test_id} should have a severity"
                    severities.add(result.severity)
            
            # Should have multiple severity levels
            assert len(severities) > 1, f"Should have multiple severity levels, got: {severities}"
            
            # Should have some high severity issues
            high_severity = [r for r in results if r.severity in [TestSeverity.CRITICAL, TestSeverity.HIGH]]
            assert len(high_severity) > 0, "Should have some high severity issues"
