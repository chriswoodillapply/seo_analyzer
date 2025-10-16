#!/usr/bin/env python3
"""
Internal Links Count Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class InternalLinksTest(SEOTest):
    """Test for internal links count"""
    
    @property
    def test_id(self) -> str:
        return "internal_links"
    
    @property
    def test_name(self) -> str:
        return "Internal Links Count"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the internal links count test"""
        soup = content.rendered_soup or content.static_soup
        links = soup.find_all('a', href=True)
        
        from urllib.parse import urlparse
        page_domain = urlparse(content.url).netloc
        
        internal_links = [
            link for link in links
            if link['href'].startswith('/') or page_domain in link['href']
        ]
        
        if 5 <= len(internal_links) <= 100:
            return TestResult(
                url=content.url,
                test_id='internal_links',
                test_name='Internal Links Count',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page has {len(internal_links)} internal links',
                recommendation='Maintain balanced internal linking structure',
                score=f'{len(internal_links)} internal links'
            )
        elif len(internal_links) < 5:
            return TestResult(
                url=content.url,
                test_id='internal_links',
                test_name='Internal Links Count',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Only {len(internal_links)} internal links found',
                recommendation='Add more internal links to improve site navigation',
                score=f'{len(internal_links)} internal links'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='internal_links',
                test_name='Internal Links Count',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Too many internal links ({len(internal_links)})',
                recommendation='Reduce number of internal links for better user experience',
                score=f'{len(internal_links)} internal links'
            )
    
