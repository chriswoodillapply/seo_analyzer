#!/usr/bin/env python3
"""
SSL Certificate Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SslCertificateTest(SEOTest):
    """Test for ssl certificate"""
    
    @property
    def test_id(self) -> str:
        return "ssl_certificate"
    
    @property
    def test_name(self) -> str:
        return "SSL Certificate"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the ssl certificate test"""
        is_https = content.url.startswith('https://')
        
        if is_https:
            return TestResult(
                url=content.url,
                test_id='ssl_certificate',
                test_name='SSL Certificate',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Critical',
                issue_description='Site uses HTTPS',
                recommendation='Continue maintaining valid SSL certificate',
                score='HTTPS enabled'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='ssl_certificate',
                test_name='SSL Certificate',
                category='Technical SEO',
                status=TestStatus.FAIL,
                severity='Critical',
                issue_description='Site uses HTTP (not secure)',
                recommendation='Implement HTTPS with valid SSL certificate immediately',
                score='HTTP only'
            )
    
