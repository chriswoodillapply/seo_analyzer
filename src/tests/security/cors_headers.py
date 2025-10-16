#!/usr/bin/env python3
"""
CORS Headers Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class CorsHeadersTest(SEOTest):
    """Test for cors headers"""
    
    @property
    def test_id(self) -> str:
        return "cors_headers"
    
    @property
    def test_name(self) -> str:
        return "CORS Headers"
    
    @property
    def category(self) -> str:
        return TestCategory.SECURITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the cors headers test"""
        headers = content.static_headers
        
        cors_header = headers.get('Access-Control-Allow-Origin', '')
        
        if cors_header:
            if cors_header == '*':
                return TestResult(
                    url=content.url,
                    test_id='cors_headers',
                    test_name='CORS Headers',
                    category='Security',
                    status=TestStatus.WARNING,
                    severity='Low',
                    issue_description='CORS allows all origins (*)',
                    recommendation='Restrict CORS to specific trusted origins',
                    score='Permissive'
                )
            else:
                return TestResult(
                    url=content.url,
                    test_id='cors_headers',
                    test_name='CORS Headers',
                    category='Security',
                    status=TestStatus.PASS,
                    severity='Low',
                    issue_description='CORS configured with specific origins',
                    recommendation='Continue maintaining restrictive CORS policy',
                    score='Restricted'
                )
        else:
            return TestResult(
                url=content.url,
                test_id='cors_headers',
                test_name='CORS Headers',
                category='Security',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No CORS headers present',
                recommendation='CORS not needed if not serving APIs',
                score='No CORS'
            )
    
