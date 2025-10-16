#!/usr/bin/env python3
"""
H1 Tag Uniqueness Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class H1UniquenessTest(SEOTest):
    """Test for h1 tag uniqueness"""
    
    @property
    def test_id(self) -> str:
        return "h1_uniqueness"
    
    @property
    def test_name(self) -> str:
        return "H1 Tag Uniqueness"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the h1 tag uniqueness test"""
        soup = content.rendered_soup or content.static_soup
        h1_tags = soup.find_all('h1')
        
        if h1_tags:
            return TestResult(
                url=content.url,
                test_id='h1_uniqueness',
                test_name='H1 Tag Uniqueness',
                category='Header Structure',
                status=TestStatus.INFO,
                severity='High',
                issue_description='H1 uniqueness check requires multi-page analysis',
                recommendation='Ensure H1 is unique across all pages',
                score='Multi-page check required'
            )
        return None
    
