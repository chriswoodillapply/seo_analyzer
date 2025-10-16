#!/usr/bin/env python3
"""
H2 Tag Presence Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class H2PresenceTest(SEOTest):
    """Test for h2 tag presence"""
    
    @property
    def test_id(self) -> str:
        return "h2_presence"
    
    @property
    def test_name(self) -> str:
        return "H2 Tag Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the h2 tag presence test"""
        soup = content.rendered_soup or content.static_soup
        h2_tags = soup.find_all('h2')
        
        if len(h2_tags) >= 2:
            return [TestResult(
                url=content.url,
                test_id='h2_presence',
                test_name='H2 Tag Presence',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page has {len(h2_tags)} H2 tags for content structure',
                recommendation='Continue using H2 tags to organize content sections',
                score=f'{len(h2_tags)} H2 tags'
            )
        elif len(h2_tags) == 0:
            return [TestResult(
                url=content.url,
                test_id='h2_presence',
                test_name='H2 Tag Presence',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No H2 tags found',
                recommendation='Add H2 tags to structure content sections',
                score='0 H2 tags'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='h2_presence',
                test_name='H2 Tag Presence',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Page has H2 tags',
                recommendation='Consider adding more H2 tags for longer content',
                score=f'{len(h2_tags)} H2 tag'
            )
    
    # =========================================================================
    # IMAGE TESTS
    # =========================================================================
    
