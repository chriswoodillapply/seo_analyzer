#!/usr/bin/env python3
"""
AMP Version Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class AmpVersionPresenceTest(SEOTest):
    """Test for amp version"""
    
    @property
    def test_id(self) -> str:
        return "amp_version_presence"
    
    @property
    def test_name(self) -> str:
        return "AMP Version"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.INFO
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the amp version test"""
        soup = content.rendered_soup or content.static_soup
        amp_link = soup.find('link', attrs={'rel': 'amphtml'})
        
        if amp_link:
            return TestResult(
                url=content.url,
                test_id='amp_version_presence',
                test_name='AMP Version',
                category='Technical SEO',
                status=TestStatus.INFO,
                severity='Info',
                issue_description='AMP version available',
                recommendation='Ensure AMP version is properly maintained',
                score='AMP available'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='amp_version_presence',
                test_name='AMP Version',
                category='Technical SEO',
                status=TestStatus.INFO,
                severity='Info',
                issue_description='No AMP version',
                recommendation='AMP is optional; focus on Core Web Vitals instead',
                score='No AMP'
            )

