#!/usr/bin/env python3
"""
Subresource Integrity (SRI) Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SubresourceIntegrityTest(SEOTest):
    """Test for subresource integrity (sri)"""
    
    @property
    def test_id(self) -> str:
        return "subresource_integrity"
    
    @property
    def test_name(self) -> str:
        return "Subresource Integrity (SRI)"
    
    @property
    def category(self) -> str:
        return TestCategory.SECURITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the subresource integrity (sri) test"""
        soup = content.rendered_soup or content.static_soup
        
        # Find external scripts and stylesheets
        external_scripts = [s for s in soup.find_all('script', src=True) 
                           if s['src'].startswith('http') and 'cdn' in s['src'].lower()]
        external_styles = [s for s in soup.find_all('link', rel='stylesheet', href=True) 
                          if s['href'].startswith('http') and 'cdn' in s['href'].lower()]
        
        total_external = len(external_scripts) + len(external_styles)
        
        if total_external == 0:
            return None
        
        with_sri = 0
        for resource in external_scripts + external_styles:
            if resource.get('integrity'):
                with_sri += 1
        
        percentage = (with_sri / total_external) * 100 if total_external else 0
        
        if percentage >= 80:
            return TestResult(
                url=content.url,
                test_id='subresource_integrity',
                test_name='Subresource Integrity (SRI)',
                category='Security',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'SRI implemented on {percentage:.0f}% of CDN resources',
                recommendation='Continue using SRI for external resources',
                score=f'{percentage:.0f}% protected'
            )
        elif percentage > 0:
            return TestResult(
                url=content.url,
                test_id='subresource_integrity',
                test_name='Subresource Integrity (SRI)',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Partial SRI implementation ({percentage:.0f}%)',
                recommendation='Add integrity attributes to all CDN resources',
                score=f'{percentage:.0f}% protected'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='subresource_integrity',
                test_name='Subresource Integrity (SRI)',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{total_external} external resources without SRI',
                recommendation='Implement SRI to protect against compromised CDNs',
                score='No SRI protection'
            )
    
