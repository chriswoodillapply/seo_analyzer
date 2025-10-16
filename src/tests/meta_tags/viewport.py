#!/usr/bin/env python3
"""
Viewport Meta Tag Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ViewportTest(SEOTest):
    """Test for viewport meta tag"""
    
    @property
    def test_id(self) -> str:
        return "viewport"
    
    @property
    def test_name(self) -> str:
        return "Viewport Meta Tag"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the viewport meta tag test"""
        soup = content.rendered_soup or content.static_soup
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        if viewport and viewport.get('content'):
            return TestResult(
                url=content.url,
                test_id='viewport_meta_tag',
                test_name='Viewport Meta Tag',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Viewport is properly configured for mobile',
                recommendation='Continue maintaining proper viewport configuration',
                score=viewport['content']
            )
        else:
            return TestResult(
                url=content.url,
                test_id='viewport_meta_tag',
                test_name='Viewport Meta Tag',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Missing viewport meta tag',
                recommendation='Add viewport meta tag for mobile responsiveness',
                score='No viewport tag'
            )
    
