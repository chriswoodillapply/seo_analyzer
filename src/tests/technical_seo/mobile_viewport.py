#!/usr/bin/env python3
"""
Mobile Viewport Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MobileViewportTest(SEOTest):
    """Test for mobile viewport"""
    
    @property
    def test_id(self) -> str:
        return "mobile_viewport"
    
    @property
    def test_name(self) -> str:
        return "Mobile Viewport"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the mobile viewport test"""
        # Inspect rendered or static soup for viewport meta tag
        soup = content.rendered_soup or content.static_soup

        if not soup:
            return self._create_result(
                content,
                TestStatus.INFO,
                'No HTML content available to inspect',
                'Ensure page can be fetched for analysis',
                'No content'
            )

        viewport = soup.find('meta', attrs={'name': 'viewport'})

        if viewport and viewport.get('content'):
            return self._create_result(
                content,
                TestStatus.PASS,
                'Viewport is properly configured for mobile',
                'Continue maintaining proper viewport configuration',
                viewport.get('content', '')
            )
        else:
            return self._create_result(
                content,
                TestStatus.FAIL,
                'Missing viewport meta tag',
                'Add viewport meta tag for mobile responsiveness',
                'No viewport tag'
            )
    
