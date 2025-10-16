#!/usr/bin/env python3
"""
Iframe Security Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class IframeSecurityTest(SEOTest):
    """Test for iframe security"""
    
    @property
    def test_id(self) -> str:
        return "iframe_security"
    
    @property
    def test_name(self) -> str:
        return "Iframe Security"
    
    @property
    def category(self) -> str:
        return TestCategory.SECURITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the iframe security test"""
        soup = content.rendered_soup or content.static_soup
        iframes = soup.find_all('iframe')
        
        if not iframes:
            return None
        
        secure_iframes = 0
        for iframe in iframes:
            if iframe.get('sandbox'):
                secure_iframes += 1
        
        percentage = (secure_iframes / len(iframes)) * 100 if iframes else 0
        
        if percentage >= 80:
            return TestResult(
                url=content.url,
                test_id='iframe_security',
                test_name='Iframe Security',
                category='Security',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{percentage:.0f}% of iframes have sandbox attribute',
                recommendation='Continue sandboxing iframes for security',
                score=f'{percentage:.0f}% sandboxed'
            )
        elif len(iframes) <= 2 and all('youtube.com' in str(iframe.get('src', '')) or 'vimeo.com' in str(iframe.get('src', '')) for iframe in iframes):
            return TestResult(
                url=content.url,
                test_id='iframe_security',
                test_name='Iframe Security',
                category='Security',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description=f'{len(iframes)} trusted iframe(s) (YouTube/Vimeo)',
                recommendation='Consider adding sandbox attributes even for trusted sources',
                score='Trusted sources'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='iframe_security',
                test_name='Iframe Security',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{len(iframes) - secure_iframes} iframes without sandbox attribute',
                recommendation='Add sandbox attribute to iframes to limit capabilities',
                score=f'{percentage:.0f}% sandboxed'
            )
    
