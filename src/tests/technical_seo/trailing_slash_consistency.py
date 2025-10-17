#!/usr/bin/env python3
"""
Trailing Slash Consistency Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class TrailingSlashConsistencyTest(SEOTest):
    """Test for trailing slash consistency"""
    
    @property
    def test_id(self) -> str:
        return "trailing_slash_consistency"
    
    @property
    def test_name(self) -> str:
        return "Trailing Slash Consistency"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the trailing slash consistency test"""
        soup = content.rendered_soup or content.static_soup
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        if not canonical:
            return None
        
        canonical_url = canonical.get('href', '')
        
        url_ends_with_slash = content.url.endswith('/')
        canonical_ends_with_slash = canonical_url.endswith('/')
        
        if url_ends_with_slash == canonical_ends_with_slash:
            return TestResult(
                url=content.url,
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='URL and canonical have consistent trailing slash usage',
                recommendation='Continue maintaining consistent URL structure',
                score='Consistent'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Trailing slash inconsistency between URL and canonical',
                recommendation='Ensure consistent trailing slash usage to avoid duplicate content',
                score='Inconsistent'
            )
    
