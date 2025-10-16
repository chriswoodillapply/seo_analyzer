#!/usr/bin/env python3
"""
Hreflang Tags Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class HreflangTagsTest(SEOTest):
    """Test for hreflang tags"""
    
    @property
    def test_id(self) -> str:
        return "hreflang_tags"
    
    @property
    def test_name(self) -> str:
        return "Hreflang Tags"
    
    @property
    def category(self) -> str:
        return TestCategory.INTERNATIONAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the hreflang tags test"""
        soup = content.rendered_soup or content.static_soup
        hreflang_tags = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
        
        if len(hreflang_tags) > 0:
            languages = [tag.get('hreflang') for tag in hreflang_tags]
            return TestResult(
                url=content.url,
                test_id='hreflang_tags',
                test_name='Hreflang Tags',
                category='International SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Found {len(hreflang_tags)} hreflang tags',
                recommendation='Ensure hreflang tags are properly implemented with reciprocal links',
                score=f'{len(hreflang_tags)} language(s): {", ".join(languages[:5])}'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='hreflang_tags',
                test_name='Hreflang Tags',
                category='International SEO',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No hreflang tags found',
                recommendation='If serving international audiences, implement hreflang tags',
                score='No hreflang'
            )
    
