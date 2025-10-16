#!/usr/bin/env python3
"""
Internal Link Quality Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class BrokenInternalLinksTest(SEOTest):
    """Test for internal link quality"""
    
    @property
    def test_id(self) -> str:
        return "broken_internal_links"
    
    @property
    def test_name(self) -> str:
        return "Internal Link Quality"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the internal link quality test"""
        from urllib.parse import urlparse, urljoin
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        internal_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or domain in href:
                internal_links.append(href)
        
        if len(internal_links) == 0:
            return []
        
        # Basic checks for obviously broken links
        suspicious_links = []
        for link in internal_links:
            # Check for common broken link patterns
            if '#' in link and link.count('#') > 1:
                suspicious_links.append(link[:50])
            elif link.endswith('//'):
                suspicious_links.append(link[:50])
        
        if suspicious_links:
            return [TestResult(
                url=content.url,
                test_id='broken_internal_links',
                test_name='Internal Link Quality',
                category='Links',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'{len(suspicious_links)} suspicious internal links found',
                recommendation='Review and fix malformed internal links',
                score=f'{len(suspicious_links)} suspicious'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='broken_internal_links',
                test_name='Internal Link Quality',
                category='Links',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'{len(internal_links)} internal links appear well-formed',
                recommendation='Continue maintaining quality internal links',
                score=f'{len(internal_links)} links OK'
            )
    
