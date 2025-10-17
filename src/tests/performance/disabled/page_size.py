#!/usr/bin/env python3
"""
Page Size Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class PageSizeTest(SEOTest):
    """Test for page size"""
    
    @property
    def test_id(self) -> str:
        return "page_size"
    
    @property
    def test_name(self) -> str:
        return "Page Size"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the page size test"""
        html = content.rendered_html or content.static_html
        size_bytes = len(html.encode('utf-8'))
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        
        if size_kb < 500:
            status = TestStatus.PASS
            issue = f'Page size is good ({size_kb:.1f} KB)'
            recommendation = 'Page size is well optimized'
        elif size_kb < 2000:
            status = TestStatus.WARNING
            issue = f'Page size is moderate ({size_kb:.1f} KB)'
            recommendation = 'Consider compressing resources for faster loading'
        else:
            status = TestStatus.FAIL
            issue = f'Page size is large ({size_mb:.2f} MB)'
            recommendation = 'Optimize and compress page resources significantly'
        
        return TestResult(
            url=content.url,
            test_id='page_size',
            test_name='Page Size',
            category='Performance',
            status=status,
            severity='Medium',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{size_kb:.1f} KB'
        )
    
