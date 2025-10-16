#!/usr/bin/env python3
"""
URL Parameters Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class UrlParametersTest(SEOTest):
    """Test for url parameters"""
    
    @property
    def test_id(self) -> str:
        return "url_parameters"
    
    @property
    def test_name(self) -> str:
        return "URL Parameters"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the url parameters test"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        
        if not parsed.query:
            return [TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Clean URL with no parameters',
                recommendation='Continue using clean URLs',
                score='0 parameters'
            )
        
        params = parsed.query.split('&')
        param_count = len(params)
        
        if param_count <= 3:
            return [TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{param_count} URL parameter(s)',
                recommendation='Parameter count is acceptable',
                score=f'{param_count} parameter(s)'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Many URL parameters ({param_count})',
                recommendation='Consider reducing parameters or using URL rewriting',
                score=f'{param_count} parameter(s)'
            )
    
