#!/usr/bin/env python3
"""
External Link Security Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ExternalLinkSecurityTest(SEOTest):
    """Test for external link security"""
    
    @property
    def test_id(self) -> str:
        return "external_link_security"
    
    @property
    def test_name(self) -> str:
        return "External Link Security"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the external link security test"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        external_links = [
            link for link in soup.find_all('a', href=True)
            if link['href'].startswith('http') and domain not in link['href']
        ]
        
        if not external_links:
            return None
        
        target_blank_links = [
            link for link in external_links
            if link.get('target') == '_blank'
        ]
        
        if not target_blank_links:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No target="_blank" on external links',
                recommendation='Current configuration is secure',
                score='No target="_blank"'
            )
        
        insecure_links = [
            link for link in target_blank_links
            if not (link.get('rel') and 
                   ('noopener' in str(link.get('rel')) or 'noreferrer' in str(link.get('rel'))))
        ]
        
        if not insecure_links:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'All {len(target_blank_links)} target="_blank" links are secure',
                recommendation='Continue using rel="noopener noreferrer" for security',
                score=f'{len(target_blank_links)} secure'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.FAIL,
                severity='Medium',
                issue_description=f'{len(insecure_links)}/{len(target_blank_links)} target="_blank" links lack security attributes',
                recommendation='Add rel="noopener noreferrer" to external links with target="_blank"',
                score=f'{len(insecure_links)} insecure'
            )
    
