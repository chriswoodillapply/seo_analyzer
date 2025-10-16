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
        return self._test_viewport(content)
    
