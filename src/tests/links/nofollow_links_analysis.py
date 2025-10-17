#!/usr/bin/env python3
"""
Nofollow Links Analysis Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class NofollowLinksAnalysisTest(SEOTest):
    """Test for nofollow links analysis"""
    
    @property
    def test_id(self) -> str:
        return "nofollow_links_analysis"
    
    @property
    def test_name(self) -> str:
        return "Nofollow Links Analysis"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the nofollow links analysis test"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        all_links = soup.find_all('a', href=True)
        
        if not all_links:
            return None
        
        nofollow_links = [
            link for link in all_links 
            if link.get('rel') and 'nofollow' in ' '.join(link.get('rel', []))
        ]
        
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        internal_nofollow = [
            link for link in nofollow_links
            if link['href'].startswith('/') or domain in link['href']
        ]
        
        if internal_nofollow:
            return TestResult(
                url=content.url,
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'{len(internal_nofollow)} internal links are nofollowed',
                recommendation='Review internal nofollow links - they may block PageRank flow',
                score=f'{len(nofollow_links)} total nofollow ({len(internal_nofollow)} internal)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'{len(nofollow_links)} external nofollow links',
                recommendation='Appropriate nofollow usage for external links',
                score=f'{len(nofollow_links)} nofollow links'
            )
    
