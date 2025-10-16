#!/usr/bin/env python3
"""
Unit tests for SEO Orchestrator with Caching Integration
"""

import pytest
import sys
import os
from datetime import datetime
from pathlib import Path
import json

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator
from src.core.test_interface import TestStatus


@pytest.fixture(scope="module")
def cached_orchestrator():
    """Fixture to provide an initialized SEOOrchestrator with caching enabled."""
    output_dir = Path("test_cached_output")
    output_dir.mkdir(exist_ok=True)
    
    with SEOOrchestrator(
        headless=True, 
        enable_javascript=True, 
        output_dir=str(output_dir), 
        verbose=True,
        enable_caching=True,
        cache_max_age_hours=24,
        save_css=True
    ) as orch:
        yield orch
    
    # Cleanup after tests
    import shutil
    if output_dir.exists():
        shutil.rmtree(output_dir)


@pytest.fixture(scope="module")
def no_cache_orchestrator():
    """Fixture to provide an initialized SEOOrchestrator with caching disabled."""
    output_dir = Path("test_no_cache_output")
    output_dir.mkdir(exist_ok=True)
    
    with SEOOrchestrator(
        headless=True, 
        enable_javascript=True, 
        output_dir=str(output_dir), 
        verbose=True,
        enable_caching=False
    ) as orch:
        yield orch
    
    # Cleanup after tests
    import shutil
    if output_dir.exists():
        shutil.rmtree(output_dir)


class TestCachedOrchestrator:
    """Test SEO Orchestrator with caching functionality."""
    
    def test_caching_enabled_by_default(self):
        """Test that caching is enabled by default."""
        output_dir = Path("test_default_cache")
        output_dir.mkdir(exist_ok=True)
        
        try:
            with SEOOrchestrator(output_dir=str(output_dir)) as orch:
                assert orch.enable_caching == True
                assert orch.content_cache is not None
                assert orch.crawl_cache is not None
                assert orch.cache_max_age_hours == 24
                assert orch.save_css == True
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_caching_can_be_disabled(self):
        """Test that caching can be explicitly disabled."""
        output_dir = Path("test_disabled_cache")
        output_dir.mkdir(exist_ok=True)
        
        try:
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=False
            ) as orch:
                assert orch.enable_caching == False
                assert orch.content_cache is None
                assert orch.crawl_cache is None
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_cache_parameters(self):
        """Test cache parameter configuration."""
        output_dir = Path("test_cache_params")
        output_dir.mkdir(exist_ok=True)
        
        try:
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True,
                cache_max_age_hours=48,
                save_css=False
            ) as orch:
                assert orch.cache_max_age_hours == 48
                assert orch.save_css == False
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_single_url_analysis_with_cache(self, cached_orchestrator):
        """Test single URL analysis with caching enabled."""
        url = "https://www.applydigital.com"
        
        # First run - should fetch and cache
        results = cached_orchestrator.analyze_single_url(url)
        
        assert len(results) > 0
        assert url in cached_orchestrator.analyzed_urls
        
        # Verify cache was created
        cache_stats = cached_orchestrator.get_cache_stats()
        assert cache_stats["caching_enabled"] == True
    
    def test_crawl_cache_functionality(self, cached_orchestrator):
        """Test crawl caching functionality."""
        start_urls = ["https://www.applydigital.com"]
        
        # First crawl - should cache results
        summary1 = cached_orchestrator.analyze_with_crawling(
            start_urls=start_urls,
            max_depth=1,
            max_urls=5,
            test_ids=None
        )
        
        assert summary1['successful'] > 0
        assert 'crawl_stats' in summary1
        
        # Second crawl with same parameters - should use cache
        summary2 = cached_orchestrator.analyze_with_crawling(
            start_urls=start_urls,
            max_depth=1,
            max_urls=5,
            test_ids=None
        )
        
        # Should have same results (from cache)
        assert summary2['successful'] == summary1['successful']
        assert summary2['crawl_stats']['total_urls'] == summary1['crawl_stats']['total_urls']
    
    def test_content_cache_functionality(self, cached_orchestrator):
        """Test content caching functionality."""
        url = "https://www.applydigital.com"
        
        # First analysis - should cache content
        results1 = cached_orchestrator.analyze_single_url(url)
        assert len(results1) > 0
        
        # Second analysis - should use cached content
        results2 = cached_orchestrator.analyze_single_url(url)
        assert len(results2) > 0
        
        # Results should be identical (from cache)
        assert len(results1) == len(results2)
    
    def test_cache_statistics(self, cached_orchestrator):
        """Test cache statistics functionality."""
        # Analyze a URL to populate cache
        cached_orchestrator.analyze_single_url("https://www.applydigital.com")
        
        # Get cache statistics
        cache_stats = cached_orchestrator.get_cache_stats()
        
        assert cache_stats["caching_enabled"] == True
        assert "content_cache" in cache_stats
        assert "crawl_cache" in cache_stats
    
    def test_clear_cache_functionality(self, cached_orchestrator):
        """Test cache clearing functionality."""
        # Analyze a URL to populate cache
        cached_orchestrator.analyze_single_url("https://www.applydigital.com")
        
        # Clear cache
        cached_orchestrator.clear_cache()
        
        # Cache should be cleared (no error should occur)
        assert True  # If we get here without error, cache clearing worked
    
    def test_report_generation_with_cache(self, cached_orchestrator):
        """Test report generation with cached data."""
        # Analyze a URL
        cached_orchestrator.analyze_single_url("https://www.applydigital.com")
        
        # Generate reports
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"test_cached_analysis_{timestamp}"
        
        report_files = cached_orchestrator.generate_reports(
            formats=['excel', 'csv', 'json'],
            base_filename=base_filename
        )
        
        assert 'excel' in report_files
        assert 'csv' in report_files
        assert 'json' in report_files
        
        # Verify files exist
        for format_type, file_path in report_files.items():
            assert Path(file_path).exists()
    
    def test_no_cache_orchestrator(self, no_cache_orchestrator):
        """Test orchestrator with caching disabled."""
        assert no_cache_orchestrator.enable_caching == False
        assert no_cache_orchestrator.content_cache is None
        assert no_cache_orchestrator.crawl_cache is None
        
        # Should still work without caching
        results = no_cache_orchestrator.analyze_single_url("https://www.applydigital.com")
        assert len(results) > 0
        
        # Cache stats should show disabled
        cache_stats = no_cache_orchestrator.get_cache_stats()
        assert cache_stats["caching_enabled"] == False
    
    def test_cache_age_expiration(self):
        """Test cache age expiration functionality."""
        output_dir = Path("test_cache_expiry")
        output_dir.mkdir(exist_ok=True)
        
        try:
            # Create orchestrator with very short cache age
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True,
                cache_max_age_hours=0.001  # Very short expiry
            ) as orch:
                # Analyze a URL
                orch.analyze_single_url("https://www.applydigital.com")
                
                # Wait a bit and analyze again - should fetch fresh content
                import time
                time.sleep(0.1)  # Wait for cache to expire
                
                results = orch.analyze_single_url("https://www.applydigital.com")
                assert len(results) > 0
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_css_caching_option(self):
        """Test CSS caching option."""
        output_dir = Path("test_css_cache")
        output_dir.mkdir(exist_ok=True)
        
        try:
            # Test with CSS caching enabled
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True,
                save_css=True
            ) as orch:
                assert orch.save_css == True
                orch.analyze_single_url("https://www.applydigital.com")
            
            # Test with CSS caching disabled
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True,
                save_css=False
            ) as orch:
                assert orch.save_css == False
                orch.analyze_single_url("https://www.applydigital.com")
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_orchestrator_context_manager(self):
        """Test orchestrator as context manager with caching."""
        output_dir = Path("test_context_cache")
        output_dir.mkdir(exist_ok=True)
        
        try:
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True
            ) as orch:
                assert orch.enable_caching == True
                assert orch.content_cache is not None
                assert orch.crawl_cache is not None
                
                # Should work normally
                results = orch.analyze_single_url("https://www.applydigital.com")
                assert len(results) > 0
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_error_handling_with_cache(self, cached_orchestrator):
        """Test error handling when caching is enabled."""
        # Test with invalid URL
        results = cached_orchestrator.analyze_single_url("https://invalid-url-that-does-not-exist.com")
        
        # Should handle gracefully
        assert isinstance(results, list)
        # May be empty due to error, which is expected
    
    def test_multiple_urls_with_cache(self, cached_orchestrator):
        """Test multiple URL analysis with caching."""
        urls = [
            "https://www.applydigital.com",
            "https://www.applydigital.com/about-us",
            "https://www.applydigital.com/services"
        ]
        
        # Analyze multiple URLs
        summary = cached_orchestrator.analyze_multiple_urls(urls)
        
        assert summary['successful'] > 0
        assert summary['total_tests'] > 0
        
        # All URLs should be in analyzed list
        for url in urls:
            assert url in cached_orchestrator.analyzed_urls or url + '/' in cached_orchestrator.analyzed_urls


class TestCacheIntegration:
    """Test cache integration edge cases."""
    
    def test_cache_directory_creation(self):
        """Test that cache directories are created properly."""
        output_dir = Path("test_cache_dirs")
        output_dir.mkdir(exist_ok=True)
        
        try:
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True
            ) as orch:
                # Cache directories should exist
                content_cache_dir = Path(orch.content_cache.cache_dir)
                crawl_cache_dir = Path(orch.crawl_cache.cache_dir)
                
                assert content_cache_dir.exists()
                assert crawl_cache_dir.exists()
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
    
    def test_cache_with_different_parameters(self):
        """Test cache behavior with different parameters."""
        output_dir = Path("test_cache_params")
        output_dir.mkdir(exist_ok=True)
        
        try:
            # Test with different cache settings
            with SEOOrchestrator(
                output_dir=str(output_dir),
                enable_caching=True,
                cache_max_age_hours=12,
                save_css=False
            ) as orch:
                assert orch.cache_max_age_hours == 12
                assert orch.save_css == False
                
                # Should work normally
                results = orch.analyze_single_url("https://www.applydigital.com")
                assert len(results) > 0
        finally:
            # Cleanup
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
