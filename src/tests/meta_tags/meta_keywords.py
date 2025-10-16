#!/usr/bin/env python3
"""
Meta Keywords (Obsolete) Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MetaKeywordsTest(SEOTest):
    """Test for meta keywords (obsolete)"""
    
    @property
    def test_id(self) -> str:
        return "meta_keywords"
    
    @property
    def test_name(self) -> str:
        return "Meta Keywords (Obsolete)"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.INFO
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the meta keywords (obsolete) test"""
        soup = content.rendered_soup or content.static_soup
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            return [TestResult(
                url=content.url,
                test_id='meta_keywords_presence',
                test_name='Meta Keywords (Obsolete)',
                category='Meta Tags',
                status=TestStatus.INFO,
                severity='Info',
                issue_description='Meta keywords tag found (not used by major search engines)',
                recommendation='Meta keywords are obsolete and can be removed',
                score=f'Present: {len(keywords)} chars'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='meta_keywords_presence',
                test_name='Meta Keywords (Obsolete)',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Info',
                issue_description='No obsolete meta keywords tag',
                recommendation='Good - meta keywords are not needed',
                score='Not present'
            )
    
