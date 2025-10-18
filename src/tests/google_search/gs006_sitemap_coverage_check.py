#!/usr/bin/env python3
"""
GS006: Sitemap Coverage Check Test

Checks sitemap presence vs indexed status using Google Search Console API
to identify sitemap indexing issues.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import json
import os
import hashlib
from datetime import datetime, timedelta


class SitemapCoverageCheckTest(SEOTest):
    """Test to check sitemap coverage using GSC API"""
    
    @property
    def test_id(self) -> str:
        return "GS006"
    
    @property
    def test_name(self) -> str:
        return "Sitemap Coverage Check"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the sitemap coverage check test"""
        results = []
        
        # Check if GSC API is available
        if not self._is_gsc_api_available():
            return [self._create_result(
                content,
                TestStatus.ERROR,
                "Google Search Console API not available",
                "Configure GSC API credentials to use this test",
                "0/100"
            )]
        
        # Get sitemap data (cached or fresh)
        sitemap_data = self._get_sitemap_data()
        
        if not sitemap_data:
            return [self._create_result(
                content,
                TestStatus.ERROR,
                "Could not retrieve sitemap data",
                "Check GSC API configuration and permissions",
                "0/100"
            )]
        
        # Check if URL is in sitemap
        in_sitemap_result = self._check_url_in_sitemap(content, sitemap_data)
        results.append(in_sitemap_result)
        
        # Check sitemap indexing status
        indexing_result = self._check_sitemap_indexing(content, sitemap_data)
        results.append(indexing_result)
        
        # Check sitemap submission status
        submission_result = self._check_sitemap_submission(content, sitemap_data)
        results.append(submission_result)
        
        return results
    
    def _is_gsc_api_available(self) -> bool:
        """Check if GSC API credentials are available"""
        return os.path.exists('credentials.json') and os.path.exists('token.pickle')
    
    def _get_sitemap_data(self) -> Optional[dict]:
        """Get sitemap data from cache or API"""
        # Check cache first
        cached_data = self._get_cached_sitemap_data()
        if cached_data:
            return cached_data
        
        # If not cached, would need to call GSC API
        # For now, return None to indicate API not implemented
        return None
    
    def _get_cached_sitemap_data(self) -> Optional[dict]:
        """Get cached sitemap data"""
        cache_dir = 'output/gsc_cache'
        cache_file = os.path.join(cache_dir, 'sitemap_data.json')
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            # Check if cache is still valid (24 hours)
            cache_time = datetime.fromisoformat(data.get('cache_timestamp', '1970-01-01'))
            if datetime.now() - cache_time > timedelta(hours=24):
                return None
            
            return data
        except:
            return None
    
    def _check_url_in_sitemap(self, content: PageContent, sitemap_data: dict) -> TestResult:
        """Check if URL is present in sitemap"""
        sitemap_urls = sitemap_data.get('sitemap_urls', [])
        
        if content.url in sitemap_urls:
            return self._create_result(
                content,
                TestStatus.PASS,
                "URL is present in sitemap",
                "URL is properly included in sitemap",
                "100/100"
            )
        
        # Check for URL variants
        url_variants = [
            content.url.rstrip('/'),
            content.url + '/',
            content.url.replace('https://', 'http://'),
            content.url.replace('www.', ''),
            content.url.replace('', 'www.')
        ]
        
        found_variants = [url for url in url_variants if url in sitemap_urls]
        
        if found_variants:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"URL variant found in sitemap: {found_variants[0]}",
                "Consider using consistent URL format in sitemap",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.FAIL,
            "URL not found in sitemap",
            "Add URL to sitemap for better discovery",
            "0/100"
        )
    
    def _check_sitemap_indexing(self, content: PageContent, sitemap_data: dict) -> TestResult:
        """Check sitemap indexing status"""
        sitemap_status = sitemap_data.get('sitemap_status', {})
        submitted_count = sitemap_status.get('submitted', 0)
        indexed_count = sitemap_status.get('indexed', 0)
        
        if indexed_count == 0 and submitted_count > 0:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Sitemap has {submitted_count} submitted URLs but 0 indexed",
                "Investigate why sitemap URLs are not being indexed",
                "0/100"
            )
        
        if indexed_count < submitted_count * 0.5:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Low sitemap indexing rate: {indexed_count}/{submitted_count}",
                "Improve content quality and fix indexing issues",
                "40/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Sitemap indexing is healthy: {indexed_count}/{submitted_count}",
            "Sitemap is being properly processed and indexed",
            "100/100"
        )
    
    def _check_sitemap_submission(self, content: PageContent, sitemap_data: dict) -> TestResult:
        """Check sitemap submission status"""
        sitemap_status = sitemap_data.get('sitemap_status', {})
        last_read = sitemap_status.get('last_read', '')
        
        if not last_read:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "No sitemap read information available",
                "Monitor sitemap submission status",
                "50/100"
            )
        
        try:
            read_time = datetime.fromisoformat(last_read.replace('Z', '+00:00'))
            days_since_read = (datetime.now(read_time.tzinfo) - read_time).days
            
            if days_since_read > 7:
                return self._create_result(
                    content,
                    TestStatus.WARNING,
                    f"Sitemap not read recently ({days_since_read} days ago)",
                    "Check sitemap submission and format",
                    "60/100"
                )
            
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Sitemap read recently ({days_since_read} days ago)",
                "Sitemap is being actively processed",
                "100/100"
            )
        except:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"Sitemap last read: {last_read}",
                "Monitor sitemap processing",
                "70/100"
            )
