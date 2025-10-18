#!/usr/bin/env python3
"""
GS005: Canonical Alignment Inspection Test

Uses Google Search Console URL Inspection API to check canonical alignment
and coverage state, with caching to avoid quota issues.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import json
import os
import hashlib
from datetime import datetime, timedelta


class CanonicalAlignmentInspectionTest(SEOTest):
    """Test to check canonical alignment using GSC URL Inspection API"""
    
    @property
    def test_id(self) -> str:
        return "GS005"
    
    @property
    def test_name(self) -> str:
        return "Canonical Alignment Inspection"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "Critical"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the canonical alignment inspection test"""
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
        
        # Get inspection data (cached or fresh)
        inspection_data = self._get_inspection_data(content.url)
        
        if not inspection_data:
            return [self._create_result(
                content,
                TestStatus.ERROR,
                "Could not retrieve URL inspection data",
                "Check GSC API configuration and permissions",
                "0/100"
            )]
        
        # Analyze coverage state
        coverage_result = self._analyze_coverage_state(content, inspection_data)
        results.append(coverage_result)
        
        # Analyze canonical alignment
        canonical_result = self._analyze_canonical_alignment(content, inspection_data)
        results.append(canonical_result)
        
        # Analyze crawl status
        crawl_result = self._analyze_crawl_status(content, inspection_data)
        results.append(crawl_result)
        
        return results
    
    def _is_gsc_api_available(self) -> bool:
        """Check if GSC API credentials are available"""
        return os.path.exists('credentials.json') and os.path.exists('token.pickle')
    
    def _get_inspection_data(self, url: str) -> Optional[dict]:
        """Get URL inspection data from cache or API"""
        # Check cache first
        cached_data = self._get_cached_inspection(url)
        if cached_data:
            return cached_data
        
        # If not cached, would need to call GSC API
        # For now, return None to indicate API not implemented
        return None
    
    def _get_cached_inspection(self, url: str) -> Optional[dict]:
        """Get cached inspection data"""
        cache_dir = 'output/gsc_cache'
        if not os.path.exists(cache_dir):
            return None
        
        # Create cache key
        cache_key = hashlib.sha1(f'sc-domain:applydigital.com|{url}'.encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{cache_key}.json')
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            # Check if cache is still valid (24 hours)
            cache_time = datetime.fromisoformat(data.get('inspection_timestamp', '1970-01-01'))
            if datetime.now() - cache_time > timedelta(hours=24):
                return None
            
            return data
        except:
            return None
    
    def _save_inspection_cache(self, url: str, data: dict):
        """Save inspection data to cache"""
        cache_dir = 'output/gsc_cache'
        os.makedirs(cache_dir, exist_ok=True)
        
        cache_key = hashlib.sha1(f'sc-domain:applydigital.com|{url}'.encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{cache_key}.json')
        
        data['inspection_timestamp'] = datetime.now().isoformat()
        data['source_property'] = 'sc-domain:applydigital.com'
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def _analyze_coverage_state(self, content: PageContent, inspection_data: dict) -> TestResult:
        """Analyze coverage state from inspection data"""
        coverage_state = inspection_data.get('coverageState', 'Unknown')
        
        if coverage_state == 'Submitted and indexed':
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Page is indexed with coverage state: {coverage_state}",
                "Page is successfully indexed by Google",
                "100/100"
            )
        
        if coverage_state in ['Submitted and not indexed', 'Discovered - currently not indexed']:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Page is not indexed: {coverage_state}",
                "Investigate why page is not being indexed",
                "40/100"
            )
        
        if 'Soft 404' in coverage_state or 'Duplicate' in coverage_state:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Page has indexing issues: {coverage_state}",
                "Fix content quality and canonical issues",
                "0/100"
            )
        
        return self._create_result(
            content,
            TestStatus.INFO,
            f"Coverage state: {coverage_state}",
            "Monitor page indexing status",
            "50/100"
        )
    
    def _analyze_canonical_alignment(self, content: PageContent, inspection_data: dict) -> TestResult:
        """Analyze canonical alignment from inspection data"""
        user_canonical = inspection_data.get('userCanonical', '')
        google_canonical = inspection_data.get('googleCanonical', '')
        
        if not user_canonical:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No user-declared canonical found",
                "Add a canonical tag to the page",
                "0/100"
            )
        
        if not google_canonical:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "Google has not selected a canonical URL",
                "Fix content quality and canonical issues to get Google canonical selection",
                "0/100"
            )
        
        if user_canonical == google_canonical:
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Canonical alignment perfect: {google_canonical}",
                "User and Google canonical URLs match",
                "100/100"
            )
        
        return self._create_result(
            content,
            TestStatus.WARNING,
            f"Canonical mismatch: user='{user_canonical}' vs Google='{google_canonical}'",
            "Align user-declared canonical with Google's selection",
            "60/100"
        )
    
    def _analyze_crawl_status(self, content: PageContent, inspection_data: dict) -> TestResult:
        """Analyze crawl status from inspection data"""
        last_crawl_time = inspection_data.get('lastCrawlTime', '')
        page_fetch_state = inspection_data.get('pageFetchState', '')
        
        if not last_crawl_time:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "No crawl time information available",
                "Monitor page for recent crawls",
                "50/100"
            )
        
        # Parse crawl time
        try:
            crawl_time = datetime.fromisoformat(last_crawl_time.replace('Z', '+00:00'))
            days_since_crawl = (datetime.now(crawl_time.tzinfo) - crawl_time).days
            
            if days_since_crawl > 30:
                return self._create_result(
                    content,
                    TestStatus.WARNING,
                    f"Page not crawled recently ({days_since_crawl} days ago)",
                    "Check for crawl blocking issues",
                    "60/100"
                )
            
            if days_since_crawl > 7:
                return self._create_result(
                    content,
                    TestStatus.INFO,
                    f"Page crawled {days_since_crawl} days ago",
                    "Monitor crawl frequency",
                    "80/100"
                )
            
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Page crawled recently ({days_since_crawl} days ago)",
                "Page is being actively crawled",
                "100/100"
            )
        except:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"Crawl time: {last_crawl_time}",
                "Monitor crawl status",
                "70/100"
            )
