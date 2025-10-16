#!/usr/bin/env python3
"""
Canonical URL Test
"""

from typing import Optional, List, TYPE_CHECKING, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class CanonicalUrlTest(SEOTest):
    """Test for canonical url"""
    
    @property
    def test_id(self) -> str:
        return "canonical_url"
    
    @property
    def test_name(self) -> str:
        return "Canonical URL"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the canonical url test"""
        soup = content.rendered_soup or content.static_soup
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        if canonical and canonical.get('href'):
            return [TestResult(
                url=content.url,
                test_id='canonical_url',
                test_name='Canonical URL',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Canonical URL is properly set',
                recommendation='Ensure canonical URL points to the preferred version',
                score=f'Points to: {canonical["href"][:50]}...'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='canonical_url',
                test_name='Canonical URL',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='High',
                issue_description='Missing canonical URL',
                recommendation='Add canonical URL to prevent duplicate content issues',
                score='No canonical tag found'
            )
    
