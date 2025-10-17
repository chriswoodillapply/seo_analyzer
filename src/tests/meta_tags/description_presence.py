#!/usr/bin/env python3
"""
Meta Description Presence Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class DescriptionPresenceTest(SEOTest):
    """Test for meta description presence"""
    
    @property
    def test_id(self) -> str:
        return "description_presence"
    
    @property
    def test_name(self) -> str:
        return "Meta Description Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the meta description presence test"""
        soup = content.rendered_soup or content.static_soup
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if meta_desc and meta_desc.get('content', '').strip():
            desc_text = meta_desc['content'].strip()
            return TestResult(
                url=content.url,
                test_id='meta_description_presence',
                test_name='Meta Description Presence',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Page has a meta description',
                recommendation='Continue maintaining unique meta descriptions',
                score=f'{len(desc_text)} characters'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='meta_description_presence',
                test_name='Meta Description Presence',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Missing or empty meta description',
                recommendation='Add unique, compelling meta description (120-160 chars)',
                score='No description found'
            )
    
