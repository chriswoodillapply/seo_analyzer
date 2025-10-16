#!/usr/bin/env python3
"""
H1 Tag Presence Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class H1PresenceTest(SEOTest):
    """Test for h1 tag presence"""
    
    @property
    def test_id(self) -> str:
        return "h1_presence"
    
    @property
    def test_name(self) -> str:
        return "H1 Tag Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the h1 tag presence test"""
        soup = content.rendered_soup or content.static_soup
        h1_tags = soup.find_all('h1')
        
        if len(h1_tags) == 1:
            return [TestResult(
                url=content.url,
                test_id='h1_presence',
                test_name='H1 Tag Presence',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Critical',
                issue_description='Page has exactly one H1 tag',
                recommendation='Continue using single H1 for main heading',
                score=f'H1: "{h1_tags[0].text.strip()[:50]}..."'
            )
        elif len(h1_tags) == 0:
            return [TestResult(
                url=content.url,
                test_id='h1_presence',
                test_name='H1 Tag Presence',
                category='Header Structure',
                status=TestStatus.FAIL,
                severity='Critical',
                issue_description='Page is missing H1 tag',
                recommendation='Add exactly one H1 tag for the main page heading',
                score='0 H1 tags'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='h1_presence',
                test_name='H1 Tag Presence',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Critical',
                issue_description=f'Page has {len(h1_tags)} H1 tags (should have 1)',
                recommendation='Use exactly one H1 tag per page',
                score=f'{len(h1_tags)} H1 tags'
            )
    
