#!/usr/bin/env python3
"""
External Links Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ExternalLinksTest(SEOTest):
    """Test for external links"""
    
    @property
    def test_id(self) -> str:
        return "external_links"
    
    @property
    def test_name(self) -> str:
        return "External Links"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the external links test"""
        soup = content.rendered_soup or content.static_soup
        links = soup.find_all('a', href=True)
        
        from urllib.parse import urlparse
        page_domain = urlparse(content.url).netloc
        
        external_links = [
            link for link in links
            if link['href'].startswith('http') and page_domain not in link['href']
        ]
        
        return TestResult(
            url=content.url,
            test_id='external_links',
            test_name='External Links',
            category='Links',
            status=TestStatus.INFO,
            severity='Low',
            issue_description=f'Page has {len(external_links)} external links',
            recommendation='Ensure external links are relevant and trustworthy',
            score=f'{len(external_links)} external links'
        )
    
