#!/usr/bin/env python3
"""
Page Title Presence Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class TitlePresenceTest(SEOTest):
    """Test for page title presence"""
    
    @property
    def test_id(self) -> str:
        return "title_presence"
    
    @property
    def test_name(self) -> str:
        return "Page Title Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the page title presence test"""
        soup = content.rendered_soup or content.static_soup
        title = soup.find('title')
        
        if title and title.text.strip():
            return [TestResult(
                url=content.url,
                test_id='meta_title_presence',
                test_name='Page Title Presence',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Critical',
                issue_description='Page has a valid title tag',
                recommendation='Continue maintaining proper title tags',
                score=f'Title: "{title.text.strip()[:50]}..."'
            )]
        else:
            return [TestResult(
                url=content.url,
                test_id='meta_title_presence',
                test_name='Page Title Presence',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='Critical',
                issue_description='Missing or empty title tag',
                recommendation='Add a descriptive, unique title tag to the page',
                score='No title found'
            )]
    
