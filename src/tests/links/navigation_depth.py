#!/usr/bin/env python3
"""
Navigation Depth Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class NavigationDepthTest(SEOTest):
    """Test for page depth from homepage"""
    
    @property
    def test_id(self) -> str:
        return "navigation_depth"
    
    @property
    def test_name(self) -> str:
        return "Page Navigation Depth"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the navigation depth test"""
        
        # If no crawl context, return INFO
        if not crawl_context:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='Requires site crawl to calculate depth from homepage',
                recommendation='Run with --crawl to enable depth analysis',
                score='Crawl required'
            )
        
        # Get page depth
        depth = crawl_context.get_page_depth(content.url)
        
        if depth == -1:
            # Page not reachable from homepage
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.FAIL,
                severity=self.severity,
                issue_description='Page is not reachable from homepage',
                recommendation='Add navigation path from homepage',
                score='Unreachable'
            )
        elif depth <= 3:
            # Good depth (0-3 clicks from homepage)
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.PASS,
                severity=self.severity,
                issue_description=f'Page is {depth} click(s) from homepage',
                recommendation='Good navigation depth for SEO',
                score=f'Depth: {depth}'
            )
        elif depth <= 5:
            # Warning (4-5 clicks)
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.WARNING,
                severity=self.severity,
                issue_description=f'Page is {depth} clicks from homepage (somewhat deep)',
                recommendation='Consider adding shortcuts or improving navigation structure',
                score=f'Depth: {depth}'
            )
        else:
            # Fail (6+ clicks)
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.FAIL,
                severity=self.severity,
                issue_description=f'Page is {depth} clicks from homepage (too deep)',
                recommendation='Improve site architecture to reduce click depth to 3 or fewer',
                score=f'Depth: {depth}'
            )
