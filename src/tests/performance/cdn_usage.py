#!/usr/bin/env python3
"""
CDN Usage Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class CdnUsageTest(SEOTest):
    """Test for cdn usage"""
    
    @property
    def test_id(self) -> str:
        return "cdn_usage"
    
    @property
    def test_name(self) -> str:
        return "CDN Usage"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the cdn usage test"""
        headers = content.static_headers
        
        # Common CDN indicators in headers
        cdn_headers = [
            'cf-ray',  # Cloudflare
            'x-amz-cf-id',  # Amazon CloudFront
            'x-cache',  # Various CDNs
            'x-cdn',
            'x-fastly-request-id',  # Fastly
            'x-akamai-transformed',  # Akamai
        ]
        
        cdn_detected = any(header.lower() in [h.lower() for h in headers.keys()] 
                          for header in cdn_headers)
        
        # Also check server header for CDN indicators
        server = headers.get('Server', '').lower()
        cdn_in_server = any(cdn in server for cdn in ['cloudflare', 'cloudfront', 'fastly', 'akamai'])
        
        if cdn_detected or cdn_in_server:
            return [TestResult(
                url=content.url,
                test_id='cdn_usage',
                test_name='CDN Usage',
                category='Performance',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='CDN detected',
                recommendation='Continue using CDN for optimal global performance',
                score='CDN in use'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='cdn_usage',
                test_name='CDN Usage',
                category='Performance',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No CDN detected',
                recommendation='Consider using a CDN to improve global load times',
                score='No CDN detected'
            )
    
