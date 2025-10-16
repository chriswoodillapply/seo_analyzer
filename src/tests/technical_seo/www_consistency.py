#!/usr/bin/env python3
"""
WWW Consistency Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class WwwConsistencyTest(SEOTest):
    """Test for www consistency"""
    
    @property
    def test_id(self) -> str:
        return "www_consistency"
    
    @property
    def test_name(self) -> str:
        return "WWW Consistency"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the www consistency test"""
        from urllib.parse import urlparse
        import requests
        
        parsed = urlparse(content.url)
        domain = parsed.netloc
        
        # Determine current version
        has_www = domain.startswith('www.')
        
        # Test the alternate version
        if has_www:
            alt_domain = domain[4:]  # Remove www.
        else:
            alt_domain = f'www.{domain}'
        
        alt_url = f'{parsed.scheme}://{alt_domain}{parsed.path}'
        
        try:
            response = requests.head(alt_url, timeout=5, allow_redirects=False)
            if response.status_code in [301, 302, 307, 308]:
                return TestResult(
                    url=content.url,
                    test_id='www_consistency',
                    test_name='WWW Consistency',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='High',
                    issue_description='Proper redirect from alternate version',
                    recommendation='Continue maintaining single canonical version',
                    score='Redirect configured'
                )
            else:
                return TestResult(
                    url=content.url,
                    test_id='www_consistency',
                    test_name='WWW Consistency',
                    category='Technical SEO',
                    status=TestStatus.WARNING,
                    severity='High',
                    issue_description='Both www and non-www versions may be accessible',
                    recommendation='Configure 301 redirect to single canonical version',
                    score='Both versions accessible'
                )
        except:
            return TestResult(
                url=content.url,
                test_id='www_consistency',
                test_name='WWW Consistency',
                category='Technical SEO',
                status=TestStatus.INFO,
                severity='High',
                issue_description='Could not verify www consistency',
                recommendation='Manually verify www/non-www redirects properly',
                score='Verification failed'
            )
    
