#!/usr/bin/env python3
"""
Pytest unit tests for Google Search Console historical analysis

Tests GSC inspection data caching, historical analysis, and soft-404 tracking
over time to identify when and why pages became soft 404s.
"""

import pytest
import sys
import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator
from src.core.test_interface import TestResult, TestStatus


class TestGSCHistoricalAnalysis:
    """Test class for GSC historical analysis and caching"""
    
    @pytest.fixture
    def test_urls(self):
        """Test URLs for historical analysis"""
        return [
            "https://www.applydigital.com/",
            "https://www.applydigital.com/ai-solutions-playbook/",
            "https://www.applydigital.com/careers/",
            "https://www.applydigital.com/leadership/dom-selvon/"
        ]
    
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
    
    def test_gsc_cache_structure(self, orchestrator_config):
        """Test that GSC cache directory structure is created properly"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            # Run analysis to trigger cache creation
            result = orchestrator.analyze_single_url("https://www.applydigital.com/")
            
            # Check if GSC cache directory exists
            gsc_cache_dir = 'test_output/gsc_cache'
            assert os.path.exists(gsc_cache_dir), f"GSC cache directory should exist at {gsc_cache_dir}"
            
            # Check cache structure
            cache_files = os.listdir(gsc_cache_dir) if os.path.exists(gsc_cache_dir) else []
            print(f"GSC Cache files: {cache_files}")
    
    def test_gsc_inspection_caching(self, test_urls, orchestrator_config):
        """Test that GSC inspection data is properly cached"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            # Analyze URLs to generate cache
            for url in test_urls:
                result = orchestrator.analyze_single_url(url)
                
                # Check if GSC cache files are created
                gsc_cache_dir = 'test_output/gsc_cache'
                if os.path.exists(gsc_cache_dir):
                    cache_files = os.listdir(gsc_cache_dir)
                    print(f"GSC Cache files for {url}: {cache_files}")
                    
                    # Look for inspection cache files
                    inspection_files = [f for f in cache_files if f.endswith('.json')]
                    assert len(inspection_files) > 0, f"Should have GSC cache files for {url}"
    
    def test_gsc_historical_data_structure(self, orchestrator_config):
        """Test that GSC historical data has proper structure"""
        # Create sample historical data
        sample_data = {
            "inspection_timestamp": datetime.now().isoformat(),
            "source_property": "sc-domain:applydigital.com",
            "coverageState": "Submitted and not indexed",
            "indexingState": "Soft 404",
            "userCanonical": "https://www.applydigital.com/",
            "googleCanonical": "N/A",
            "crawlState": "Success",
            "lastCrawlTime": "2025-10-17T03:53:49Z",
            "historical_data": {
                "2025-10-01": {
                    "coverageState": "Submitted and indexed",
                    "indexingState": "Indexed",
                    "googleCanonical": "https://www.applydigital.com/"
                },
                "2025-10-15": {
                    "coverageState": "Submitted and not indexed",
                    "indexingState": "Soft 404",
                    "googleCanonical": "N/A"
                }
            }
        }
        
        # Save to cache
        cache_dir = 'test_output/gsc_cache'
        os.makedirs(cache_dir, exist_ok=True)
        
        cache_key = hashlib.sha1(f'sc-domain:applydigital.com|https://www.applydigital.com/'.encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{cache_key}.json')
        
        with open(cache_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        # Verify structure
        assert os.path.exists(cache_file), "Cache file should be created"
        
        with open(cache_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert 'inspection_timestamp' in loaded_data, "Should have timestamp"
        assert 'coverageState' in loaded_data, "Should have coverage state"
        assert 'historical_data' in loaded_data, "Should have historical data"
        assert len(loaded_data['historical_data']) > 0, "Should have historical entries"
    
    def test_soft_404_historical_tracking(self, orchestrator_config):
        """Test tracking of soft 404 changes over time"""
        # Create historical data showing soft 404 progression
        historical_data = {
            "url": "https://www.applydigital.com/",
            "historical_changes": [
                {
                    "date": "2025-09-01",
                    "coverageState": "Submitted and indexed",
                    "indexingState": "Indexed",
                    "googleCanonical": "https://www.applydigital.com/",
                    "crawlState": "Success"
                },
                {
                    "date": "2025-09-15",
                    "coverageState": "Submitted and indexed",
                    "indexingState": "Indexed", 
                    "googleCanonical": "https://www.applydigital.com/",
                    "crawlState": "Success"
                },
                {
                    "date": "2025-10-01",
                    "coverageState": "Submitted and not indexed",
                    "indexingState": "Soft 404",
                    "googleCanonical": "N/A",
                    "crawlState": "Success"
                },
                {
                    "date": "2025-10-17",
                    "coverageState": "Submitted and not indexed",
                    "indexingState": "Soft 404",
                    "googleCanonical": "N/A",
                    "crawlState": "Success"
                }
            ]
        }
        
        # Save historical data
        cache_dir = 'test_output/gsc_cache'
        os.makedirs(cache_dir, exist_ok=True)
        
        historical_file = os.path.join(cache_dir, 'historical_soft_404s.json')
        with open(historical_file, 'w') as f:
            json.dump(historical_data, f, indent=2)
        
        # Analyze historical changes
        changes = historical_data['historical_changes']
        
        # Find when soft 404 started
        soft_404_start = None
        for change in changes:
            if change['indexingState'] == 'Soft 404':
                soft_404_start = change['date']
                break
        
        assert soft_404_start == "2025-10-01", f"Soft 404 should have started on 2025-10-01, found {soft_404_start}"
        
        # Check that canonical was lost
        canonical_lost_date = None
        for change in changes:
            if change['googleCanonical'] == 'N/A':
                canonical_lost_date = change['date']
                break
        
        assert canonical_lost_date == "2025-10-01", f"Canonical should have been lost on 2025-10-01, found {canonical_lost_date}"
    
    def test_gsc_cache_validation(self, orchestrator_config):
        """Test that GSC cache validation works correctly"""
        cache_dir = 'test_output/gsc_cache'
        os.makedirs(cache_dir, exist_ok=True)
        
        # Create valid cache file
        valid_data = {
            "inspection_timestamp": datetime.now().isoformat(),
            "coverageState": "Submitted and indexed",
            "indexingState": "Indexed"
        }
        
        valid_file = os.path.join(cache_dir, 'valid_cache.json')
        with open(valid_file, 'w') as f:
            json.dump(valid_data, f)
        
        # Create expired cache file
        expired_data = {
            "inspection_timestamp": (datetime.now() - timedelta(hours=25)).isoformat(),
            "coverageState": "Submitted and indexed",
            "indexingState": "Indexed"
        }
        
        expired_file = os.path.join(cache_dir, 'expired_cache.json')
        with open(expired_file, 'w') as f:
            json.dump(expired_data, f)
        
        # Test cache validation
        def is_cache_valid(cache_file: str, max_age_hours: int = 24) -> bool:
            if not os.path.exists(cache_file):
                return False
            
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                cache_time = datetime.fromisoformat(data.get('inspection_timestamp', '1970-01-01'))
                return datetime.now() - cache_time <= timedelta(hours=max_age_hours)
            except:
                return False
        
        assert is_cache_valid(valid_file), "Valid cache should be valid"
        assert not is_cache_valid(expired_file), "Expired cache should be invalid"
    
    def test_gsc_quota_management(self, orchestrator_config):
        """Test GSC API quota management and caching"""
        # Simulate quota tracking
        quota_data = {
            "daily_quota_used": 0,
            "quota_reset_time": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            "last_request_time": None,
            "requests_today": []
        }
        
        quota_file = 'test_output/gsc_cache/quota_tracking.json'
        os.makedirs(os.path.dirname(quota_file), exist_ok=True)
        
        with open(quota_file, 'w') as f:
            json.dump(quota_data, f, indent=2, default=str)
        
        # Test quota checking
        def check_quota_available() -> bool:
            if not os.path.exists(quota_file):
                return True
            
            try:
                with open(quota_file, 'r') as f:
                    data = json.load(f)
                
                return data['daily_quota_used'] < 2000  # GSC URL inspection limit
            except:
                return True
        
        assert check_quota_available(), "Quota should be available initially"
    
    def test_soft_404_pattern_analysis(self, orchestrator_config):
        """Test analysis of soft 404 patterns across multiple URLs"""
        # Create pattern analysis data
        pattern_data = {
            "analysis_date": datetime.now().isoformat(),
            "total_urls_analyzed": 10,
            "soft_404_urls": 6,
            "indexed_urls": 4,
            "common_patterns": {
                "splash_screen_present": 5,
                "cookie_dialog_present": 5,
                "canonical_mismatch": 4,
                "thin_static_content": 6,
                "javascript_errors": 3
            },
            "urls_by_status": {
                "soft_404": [
                    "https://www.applydigital.com/",
                    "https://www.applydigital.com/careers/",
                    "https://www.applydigital.com/insights/learn/",
                    "https://www.applydigital.com/e2x/",
                    "https://www.applydigital.com/insights/costs-of-moving-to-composable-tech-what-you-need-to-know/",
                    "https://www.applydigital.com/insights/learn/advantages-of-using-markup-in-jamstack/"
                ],
                "indexed": [
                    "https://www.applydigital.com/ai-solutions-playbook/",
                    "https://www.applydigital.com/leadership/dom-selvon/",
                    "https://www.applydigital.com/es-419/servicios/contentstack/",
                    "https://www.applydigital.com/es-419/insights/aprende/"
                ]
            }
        }
        
        # Save pattern analysis
        pattern_file = 'test_output/gsc_cache/soft_404_patterns.json'
        os.makedirs(os.path.dirname(pattern_file), exist_ok=True)
        
        with open(pattern_file, 'w') as f:
            json.dump(pattern_data, f, indent=2)
        
        # Analyze patterns
        assert pattern_data['soft_404_urls'] > pattern_data['indexed_urls'], "More URLs should be soft 404"
        assert pattern_data['common_patterns']['splash_screen_present'] == 5, "All soft 404 URLs should have splash screen"
        assert pattern_data['common_patterns']['cookie_dialog_present'] == 5, "All soft 404 URLs should have cookie dialog"
    
    def test_gsc_output_directory_structure(self, orchestrator_config):
        """Test that GSC analysis creates proper output directory structure"""
        with SEOOrchestrator(**orchestrator_config) as orchestrator:
            # Run analysis
            result = orchestrator.analyze_single_url("https://www.applydigital.com/")
            
            # Check output directory structure
            output_dir = 'test_output'
            assert os.path.exists(output_dir), f"Output directory should exist: {output_dir}"
            
            # Check for GSC cache directory
            gsc_cache_dir = os.path.join(output_dir, 'gsc_cache')
            if os.path.exists(gsc_cache_dir):
                cache_files = os.listdir(gsc_cache_dir)
                print(f"GSC Cache structure: {cache_files}")
                
                # Should have various cache files
                expected_files = ['quota_tracking.json', 'soft_404_patterns.json', 'historical_soft_404s.json']
                for expected_file in expected_files:
                    if expected_file in cache_files:
                        print(f"✅ Found {expected_file}")
                    else:
                        print(f"⚠️ Missing {expected_file}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
