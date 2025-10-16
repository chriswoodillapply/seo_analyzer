#!/usr/bin/env python3
"""
Favicon Presence Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class FaviconPresenceTest(SEOTest):
    """Test for favicon presence"""
    
    @property
    def test_id(self) -> str:
        return "favicon_presence"
    
    @property
    def test_name(self) -> str:
        return "Favicon Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the favicon presence test"""
        soup = content.rendered_soup or content.static_soup
        favicon = (
            soup.find('link', attrs={'rel': 'icon'}) or
            soup.find('link', attrs={'rel': 'shortcut icon'}) or
            soup.find('link', attrs={'rel': 'apple-touch-icon'})
        )
        
        if favicon:
            return TestResult(
                url=content.url,
                test_id='favicon_presence',
                test_name='Favicon Presence',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Favicon is present',
                recommendation='Continue providing favicon for brand recognition',
                score='Favicon found'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='favicon_presence',
                test_name='Favicon Presence',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='No favicon detected',
                recommendation='Add favicon to improve brand recognition in browser tabs and bookmarks',
                score='No favicon'
            )


    
    # =========================================================================
    # ADDITIONAL HEADER TESTS - PHASE 1
    # =========================================================================
    
