#!/usr/bin/env python3
"""
Compression Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class GzipCompressionTest(SEOTest):
    """Test for compression"""
    
    @property
    def test_id(self) -> str:
        return "gzip_compression"
    
    @property
    def test_name(self) -> str:
        return "Compression"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the compression test"""
        headers = content.static_headers
        
        encoding = headers.get('Content-Encoding', '').lower()
        
        if 'gzip' in encoding or 'br' in encoding:
            return TestResult(
                url=content.url,
                test_id='gzip_compression',
                test_name='Compression',
                category='Performance',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Response is compressed ({encoding})',
                recommendation='Continue using compression for optimal performance',
                score=f'{encoding} enabled'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='gzip_compression',
                test_name='Compression',
                category='Performance',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No compression detected',
                recommendation='Enable gzip or brotli compression to reduce file size by 60-80%',
                score='No compression'
            )
    
